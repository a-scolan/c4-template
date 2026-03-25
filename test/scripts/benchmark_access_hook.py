from __future__ import annotations

import importlib.util
import json
import os
import sys
from pathlib import Path
from typing import Any

_SCRIPTS_DIR = str(Path(__file__).resolve().parent)
if _SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, _SCRIPTS_DIR)

from benchmark.hook_runtime import (
    anonymous_session_context,
    append_additional_context,
    bool_env_enabled,
    extract_tool_paths,
    fixed_collect_path_like_values,
    normalize_payload_session,
    permission_decision,
    permission_reason,
    reset_session_state,
    resolve_effective_session_id,
    resolve_workspace_root,
    uses_anonymous_session,
    write_resolved_audit_record,
)


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


def infer_anonymous_session_suffix(payload: dict[str, Any], workspace_root: Path, mode: str) -> str | None:
    tool_paths = extract_tool_paths(payload, workspace_root, legacy)
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


legacy.collect_path_like_values = lambda obj, parent_key="": fixed_collect_path_like_values(obj, parent_key, legacy=legacy)


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
    for rel_path in extract_tool_paths(payload, workspace_root, legacy):
        normalized = rel_path.replace("\\", "/").lstrip("/")
        iteration_name: str | None = None

        if normalized.endswith("/blind/A.md") or normalized.endswith("/blind/B.md"):
            iteration_name = legacy.extract_iteration_from_iteration_path(normalized)
        else:
            parts = normalized.split("/")
            if (
                len(parts) >= 7
                and parts[0] == "test"
                and legacy.is_benchmark_iteration_dir(parts[1])
                and parts[-3] == "blind"
                and parts[-2].startswith("run-")
                and parts[-1] in {"A.md", "B.md"}
            ):
                iteration_name = parts[1]
            elif (
                len(parts) >= 5
                and parts[0] == "test"
                and legacy.is_benchmark_iteration_dir(parts[1])
                and "blind" in parts
                and parts.index("blind") >= 4
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
        normalized_payload = normalize_payload_session(payload, mode, workspace_root, legacy=legacy)
        raw_session_id = payload.get("sessionId")
        effective_session_id = str(normalized_payload.get("sessionId", "default"))

        legacy.maybe_write_debug(payload, mode)

        if event_name == "SessionStart":
            reset_session_state(workspace_root, effective_session_id, mode, legacy=legacy)
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

        write_resolved_audit_record(payload, normalized_payload, mode, workspace_root, result, decision_source, legacy=legacy)
        legacy.emit(result)
    except Exception as exc:  # pragma: no cover - safety belt for hook runtime
        print(f"benchmark hook failure: {exc}", file=sys.stderr)
        raise SystemExit(2)


if __name__ == "__main__":
    main()