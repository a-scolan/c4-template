from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any


AUDIT_LOG_FILENAME = "hook-audit.jsonl"
ENABLED_BOOL_VALUES = {"1", "true", "yes", "on"}
ANONYMOUS_SESSION_PREFIX = "anonymous-"
STATEFUL_ANONYMOUS_MODES = {"baseline", "baseline_hook_only", "with_skill_targeted", "blind_compare"}
TRACE_LEVEL_ALIASES = {
	"0": "off",
	"off": "off",
	"none": "off",
	"quiet": "off",
	"minimal": "off",
	"normal": "off",
	"1": "audit",
	"audit": "audit",
	"info": "audit",
	"2": "debug",
	"debug": "debug",
	"trace": "debug",
	"verbose": "debug",
}


def resolve_workspace_root(payload: dict[str, Any]) -> Path:
	cwd = payload.get("cwd") or "."
	try:
		return Path(cwd).resolve()
	except Exception:
		return Path(".").resolve()


def bool_env_enabled(name: str) -> bool:
	return os.environ.get(name, "").strip().lower() in ENABLED_BOOL_VALUES


def resolve_trace_level() -> str:
	explicit = os.environ.get("BENCH_TRACE_LEVEL", "").strip().lower()
	if explicit:
		return TRACE_LEVEL_ALIASES.get(explicit, "off")
	if bool_env_enabled("BENCH_DEBUG_HOOKS"):
		return "debug"
	if os.environ.get("BENCH_AUDIT_LOG", "").strip():
		return "audit"
	return "off"


def infer_anonymous_session_suffix(payload: dict[str, Any], workspace_root: Path, mode: str, legacy: Any) -> str | None:
	tool_paths = extract_tool_paths(payload, workspace_root, legacy)
	if not tool_paths:
		return None

	if mode == "with_skill_targeted":
		skills = {
			skill
			for rel_path in tool_paths
			if (skill := legacy.extract_skill_from_skills_path(rel_path) or legacy.extract_skill_from_iteration_path(rel_path))
		}
		if len(skills) == 1:
			return f"{mode}-{next(iter(skills))}"
		return None

	if mode in {"baseline", "baseline_hook_only"}:
		iterations = {
			iteration
			for rel_path in tool_paths
			if (iteration := legacy.extract_iteration_from_iteration_path(rel_path))
		}
		if len(iterations) == 1:
			return f"{mode}-{next(iter(iterations))}"
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
	*,
	legacy: Any,
) -> str:
	if isinstance(session_id, str) and session_id.strip():
		return session_id.strip()
	if payload is not None and workspace_root is not None and mode in STATEFUL_ANONYMOUS_MODES:
		derived_suffix = infer_anonymous_session_suffix(payload, workspace_root, mode, legacy)
		if derived_suffix:
			return f"{ANONYMOUS_SESSION_PREFIX}{derived_suffix}"
	if mode:
		return f"{ANONYMOUS_SESSION_PREFIX}{mode}"
	return "default"


def uses_anonymous_session(raw_session_id: Any, effective_session_id: str) -> bool:
	return not (isinstance(raw_session_id, str) and raw_session_id.strip()) and bool(effective_session_id)


def normalize_payload_session(payload: dict[str, Any], mode: str, workspace_root: Path, *, legacy: Any) -> dict[str, Any]:
	normalized = dict(payload)
	normalized["sessionId"] = resolve_effective_session_id(payload.get("sessionId"), mode, payload, workspace_root, legacy=legacy)
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

	if resolve_trace_level() not in {"audit", "debug"}:
		return None

	debug_log = os.environ.get("BENCH_DEBUG_LOG", "").strip()
	if debug_log:
		return resolve_log_path(debug_log, workspace_root).with_name(AUDIT_LOG_FILENAME)

	return workspace_root / "test" / "_agent-hooks" / AUDIT_LOG_FILENAME


def fixed_collect_path_like_values(obj: Any, parent_key: str = "", *, legacy: Any) -> list[str]:
	values: list[str] = []
	if isinstance(obj, dict):
		for key, value in obj.items():
			key_lower = key.lower()
			if isinstance(value, str) and key_lower in legacy.PATHISH_KEYS:
				values.append(value)
			else:
				values.extend(fixed_collect_path_like_values(value, key_lower, legacy=legacy))
	elif isinstance(obj, list):
		for item in obj:
			values.extend(fixed_collect_path_like_values(item, parent_key, legacy=legacy))
	elif isinstance(obj, str) and parent_key in legacy.PATHISH_KEYS:
		values.append(obj)
	return values


def reset_session_state(workspace_root: Path, session_id: str, mode: str, *, legacy: Any) -> None:
	legacy.save_state(
		workspace_root,
		{
			"mode": mode,
			"session_id": session_id,
		},
	)


def extract_tool_paths(payload: dict[str, Any], workspace_root: Path, legacy: Any) -> list[str]:
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
	*,
	legacy: Any,
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
		"tool_paths": extract_tool_paths(payload, workspace_root, legacy),
		"permissionDecision": permission_decision(output),
		"permissionDecisionReason": permission_reason(output),
		"decisionSource": decision_source,
	}
	with log_path.open("a", encoding="utf-8") as handle:
		handle.write(json.dumps(record, ensure_ascii=False) + "\n")
