from __future__ import annotations

import importlib.util
import json
import os
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
LEGACY_HOOK_PATH = ROOT / ".github" / "agents" / "scripts" / "enforce-test-access.py"
RESTRICTED_LIKEC4_MCP_NAMES = {
    "mcplikec4listprojects",
    "mcplikec4readprojectsummary",
    "mcplikec4readview",
    "mcplikec4openview",
}
AUDIT_LOG_FILENAME = "hook-audit.jsonl"
ENABLED_BOOL_VALUES = {"1", "true", "yes", "on"}
ANONYMOUS_SESSION_PREFIX = "anonymous-"
STATEFUL_ANONYMOUS_MODES = {"with_skill_targeted", "blind_compare"}


def load_legacy_hook_module():
    spec = importlib.util.spec_from_file_location("legacy_benchmark_hook", LEGACY_HOOK_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load legacy benchmark hook: {LEGACY_HOOK_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


legacy = load_legacy_hook_module()


def resolve_workspace_root(payload: dict[str, Any]) -> Path:
    cwd = payload.get("cwd") or "."
    try:
        return Path(cwd).resolve()
    except Exception:
        return Path(".").resolve()


def bool_env_enabled(name: str) -> bool:
    return os.environ.get(name, "").strip().lower() in ENABLED_BOOL_VALUES


def infer_anonymous_session_suffix(payload: dict[str, Any], workspace_root: Path, mode: str) -> str | None:
    tool_paths = extract_tool_paths(payload, workspace_root)
    if not tool_paths:
        return None

    if mode == "with_skill_targeted":
        skills = {
            skill
            for rel_path in tool_paths
            if (skill := legacy.extract_skill_from_skills_path(rel_path))
        }
        if len(skills) == 1:
            return f"{mode}-{next(iter(skills))}"
        return None

    if mode == "blind_compare":
        skills: set[str] = set()
        iterations: set[str] = set()
        for rel_path in tool_paths:
            normalized = rel_path.replace("\\", "/").lstrip("/")
            skill = legacy.extract_skill_from_skills_path(normalized) or legacy.extract_skill_from_iteration_path(normalized)
            if skill:
                skills.add(skill)

            iteration = legacy.extract_iteration_from_iteration_path(normalized)
            if iteration:
                iterations.add(iteration)

        if len(skills) > 1 or len(iterations) > 1:
            return None

        skill_part = next(iter(skills)) if skills else "unknown-skill"
        if iterations:
            return f"{mode}-{next(iter(iterations))}-{skill_part}"
        if skills:
            return f"{mode}-{skill_part}"
        return None

    return None


def resolve_effective_session_id(
    session_id: Any,
    mode: str,
    payload: dict[str, Any] | None = None,
    workspace_root: Path | None = None,
) -> str:
    if isinstance(session_id, str) and session_id.strip():
        return session_id.strip()
    if payload is not None and workspace_root is not None and mode in STATEFUL_ANONYMOUS_MODES:
        derived_suffix = infer_anonymous_session_suffix(payload, workspace_root, mode)
        if derived_suffix:
            return f"{ANONYMOUS_SESSION_PREFIX}{derived_suffix}"
    if mode:
        return f"{ANONYMOUS_SESSION_PREFIX}{mode}"
    return "default"


def uses_anonymous_session(raw_session_id: Any, effective_session_id: str) -> bool:
    return not (isinstance(raw_session_id, str) and raw_session_id.strip()) and bool(effective_session_id)


def normalize_payload_session(payload: dict[str, Any], mode: str, workspace_root: Path) -> dict[str, Any]:
    normalized = dict(payload)
    normalized["sessionId"] = resolve_effective_session_id(payload.get("sessionId"), mode, payload, workspace_root)
    return normalized


def append_additional_context(output: dict[str, Any], context: str | None) -> dict[str, Any]:
    if not context:
        return output

    hook_output = output.get("hookSpecificOutput")
    if not isinstance(hook_output, dict):
        hook_output = {}
    else:
        hook_output = dict(hook_output)

    existing = hook_output.get("additionalContext")
    if isinstance(existing, str) and existing.strip():
        hook_output["additionalContext"] = f"{existing} {context}".strip()
    else:
        hook_output["additionalContext"] = context
    return {"hookSpecificOutput": hook_output}


def anonymous_session_context(mode: str, raw_session_id: Any, effective_session_id: str) -> str | None:
    if not uses_anonymous_session(raw_session_id, effective_session_id):
        return None
    if mode in STATEFUL_ANONYMOUS_MODES:
        default_shared_session = f"{ANONYMOUS_SESSION_PREFIX}{mode}"
        if effective_session_id != default_shared_session:
            return (
                f"No sessionId was provided in the hook payload, so the hook derived the anonymous session '{effective_session_id}' "
                "from the requested benchmark scope."
            )
        return (
            f"No sessionId was provided in the hook payload, so the hook is using the shared anonymous session '{effective_session_id}'. "
            "Run this stateful benchmark phase serially and reset hook state between fresh workers."
        )
    return f"No sessionId was provided in the hook payload, so the hook is using the anonymous session '{effective_session_id}'."


def resolve_log_path(path_value: str, workspace_root: Path) -> Path:
    path = Path(path_value)
    if not path.is_absolute():
        path = workspace_root / path
    return path


def resolve_audit_log_path(workspace_root: Path) -> Path | None:
    explicit = os.environ.get("BENCH_AUDIT_LOG", "").strip()
    if explicit:
        return resolve_log_path(explicit, workspace_root)

    if not bool_env_enabled("BENCH_DEBUG_HOOKS"):
        return None

    debug_log = os.environ.get("BENCH_DEBUG_LOG", "").strip()
    if debug_log:
        return resolve_log_path(debug_log, workspace_root).with_name(AUDIT_LOG_FILENAME)

    return workspace_root / "test" / "_agent-hooks" / AUDIT_LOG_FILENAME


def fixed_collect_path_like_values(obj: Any, parent_key: str = "") -> list[str]:
    values: list[str] = []
    if isinstance(obj, dict):
        for key, value in obj.items():
            key_lower = key.lower()
            if isinstance(value, str) and key_lower in legacy.PATHISH_KEYS:
                values.append(value)
            else:
                values.extend(fixed_collect_path_like_values(value, key_lower))
    elif isinstance(obj, list):
        for item in obj:
            values.extend(fixed_collect_path_like_values(item, parent_key))
    elif isinstance(obj, str) and parent_key in legacy.PATHISH_KEYS:
        values.append(obj)
    return values


def reset_session_state(workspace_root: Path, session_id: str, mode: str) -> None:
    legacy.save_state(
        workspace_root,
        {
            "mode": mode,
            "session_id": session_id,
        },
    )


legacy.collect_path_like_values = fixed_collect_path_like_values


def extract_tool_paths(payload: dict[str, Any], workspace_root: Path) -> list[str]:
    tool_name = str(payload.get("tool_name", ""))
    tool_input = payload.get("tool_input")
    if tool_input is None:
        return []
    try:
        return legacy.extract_paths(tool_name, tool_input, workspace_root)
    except Exception:
        return []


def permission_decision(output: dict[str, Any]) -> str:
    hook_output = output.get("hookSpecificOutput", {})
    decision = hook_output.get("permissionDecision")
    if isinstance(decision, str) and decision.strip():
        return decision.strip()
    if output.get("continue") is True:
        return "allow"
    return "unknown"


def permission_reason(output: dict[str, Any]) -> str | None:
    hook_output = output.get("hookSpecificOutput", {})
    reason = hook_output.get("permissionDecisionReason")
    if isinstance(reason, str) and reason.strip():
        return reason.strip()
    return None


def write_resolved_audit_record(
    raw_payload: dict[str, Any],
    payload: dict[str, Any],
    mode: str,
    workspace_root: Path,
    output: dict[str, Any],
    decision_source: str,
) -> None:
    log_path = resolve_audit_log_path(workspace_root)
    if log_path is None:
        return

    log_path.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "timestamp": raw_payload.get("timestamp"),
        "hookEventName": raw_payload.get("hookEventName") or legacy.infer_hook_event_name(raw_payload),
        "mode": mode,
        "sessionId": raw_payload.get("sessionId"),
        "effectiveSessionId": payload.get("sessionId"),
        "anonymousSessionFallback": uses_anonymous_session(raw_payload.get("sessionId"), str(payload.get("sessionId", ""))),
        "tool_name": str(raw_payload.get("tool_name", "")),
        "tool_paths": extract_tool_paths(payload, workspace_root),
        "permissionDecision": permission_decision(output),
        "permissionDecisionReason": permission_reason(output),
        "decisionSource": decision_source,
    }
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def normalize_tool_name(tool_name: str) -> str:
    return "".join(character for character in tool_name.lower() if character.isalnum())


def deny_restricted_likec4_mcp(tool_name: str, mode: str) -> dict[str, Any] | None:
    if mode not in {"baseline", "baseline_hook_only", "with_skill_targeted"}:
        return None
    normalized = normalize_tool_name(tool_name)
    if normalized not in RESTRICTED_LIKEC4_MCP_NAMES:
        return None
    return legacy.deny(
        "This LikeC4 MCP tool is too broad for scored benchmark workers. "
        "Project listing, project summaries, and view browsing are denied; keep MCP usage limited to narrow element/relationship grounding."
    )


def blind_compare_iteration_override(payload: dict[str, Any], workspace_root: Path, mode: str) -> str | None:
    if mode != "blind_compare":
        return None

    iterations: set[str] = set()
    for rel_path in extract_tool_paths(payload, workspace_root):
        normalized = rel_path.replace("\\", "/").lstrip("/")
        iteration_name: str | None = None

        if normalized.endswith("/blind/A.md") or normalized.endswith("/blind/B.md"):
            iteration_name = legacy.extract_iteration_from_iteration_path(normalized)
        else:
            parts = normalized.split("/")
            if (
                len(parts) >= 7
                and parts[0] == "test"
                and legacy.ITERATION_RE.match(parts[1])
                and parts[-3] == "blind"
                and parts[-2].startswith("run-")
                and parts[-1] in {"A.md", "B.md"}
            ):
                iteration_name = parts[1]

        if iteration_name:
            iterations.add(iteration_name)

    if not iterations:
        return None
    if len(iterations) > 1:
        raise ValueError("Blind comparator tool use may reference only one benchmark iteration at a time.")
    return next(iter(iterations))


def main() -> None:
    try:
        raw = sys.stdin.read().strip()
        payload = json.loads(raw) if raw else {}
        event_name = legacy.infer_hook_event_name(payload)
        mode = os.environ.get("BENCH_MODE", "").strip()
        workspace_root = resolve_workspace_root(payload)
        normalized_payload = normalize_payload_session(payload, mode, workspace_root)
        raw_session_id = payload.get("sessionId")
        effective_session_id = str(normalized_payload.get("sessionId", "default"))

        legacy.maybe_write_debug(payload, mode)

        if event_name == "SessionStart":
            reset_session_state(workspace_root, effective_session_id, mode)
            session_output = append_additional_context(
                legacy.session_start_output(mode),
                anonymous_session_context(mode, raw_session_id, effective_session_id),
            )
            legacy.emit(session_output)
            return
        if event_name == "SubagentStart":
            legacy.emit(legacy.subagent_start_output(mode))
            return
        if event_name != "PreToolUse":
            legacy.emit(legacy.common_allow())
            return

        tool_name = str(normalized_payload.get("tool_name", ""))
        restricted_mcp_denial = deny_restricted_likec4_mcp(tool_name, mode)
        decision_source = "legacy-policy"
        if restricted_mcp_denial is not None:
            result = restricted_mcp_denial
            decision_source = "wrapper-restricted-likec4-mcp"
        else:
            try:
                requested_iteration = blind_compare_iteration_override(normalized_payload, workspace_root, mode)
            except ValueError as exc:
                result = legacy.deny(str(exc))
                decision_source = "wrapper-blind-iteration-deny"
            else:
                if requested_iteration is None:
                    result = legacy.handle_pre_tool_use(normalized_payload, mode)
                else:
                    original_latest_iteration_name = legacy.latest_iteration_name
                    try:
                        legacy.latest_iteration_name = lambda _workspace_root, override=requested_iteration: override
                        result = legacy.handle_pre_tool_use(normalized_payload, mode)
                    finally:
                        legacy.latest_iteration_name = original_latest_iteration_name
                    decision_source = "wrapper-blind-iteration-override"

        write_resolved_audit_record(payload, normalized_payload, mode, workspace_root, result, decision_source)
        legacy.emit(result)
    except Exception as exc:  # pragma: no cover - safety belt for hook runtime
        print(f"benchmark hook failure: {exc}", file=sys.stderr)
        raise SystemExit(2)


if __name__ == "__main__":
    main()