from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlparse

ITERATION_RE = re.compile(r"^iteration-\d+$")
SERIES_ITERATION_RE = re.compile(r"^.+-test\d+$")
PATCH_PATH_RE = re.compile(r"^\*\*\* (?:Add|Update|Delete) File: (.+)$", re.MULTILINE)
WILDCARD_RE = re.compile(r"[*?\[{]")

READ_ONLY_TOOL_NAMES = {
    "read_file",
    "get_errors",
    "copilot_getNotebookSummary",
    "get_changed_files",
}
SEARCH_TOOL_NAMES = {
    "grep_search",
    "file_search",
    "semantic_search",
}
EDIT_TOOL_NAMES = {
    "apply_patch",
    "create_file",
    "create_directory",
    "edit_notebook_file",
    "create_new_jupyter_notebook",
    "replace_string_in_file",
    "multi_replace_string_in_file",
}
EXECUTE_TOOL_NAMES = {
    "run_in_terminal",
    "await_terminal",
    "get_terminal_output",
    "kill_terminal",
    "create_and_run_task",
    "run_vscode_command",
}
WEB_TOOL_NAMES = {
    "fetch_webpage",
    "open_browser_page",
}
AGENT_TOOL_NAMES = {
    "runSubagent",
}
SAFE_META_TOOL_NAMES = {
    "manage_todo_list",
}
ALLOWED_LIKEC4_MCP_MODES = {
    "baseline",
    "baseline_hook_only",
    "with_skill_targeted",
}
ALLOWED_LIKEC4_MCP_PREFIX = "mcplikec4"
EXTERNAL_PATH_TAG = "@external/"
FORBIDDEN_NON_WORKER_PREFIXES = (
    ".github/prompts/",
    ".github/instructions/",
    ".github/hooks/",
)
ROOT_READ_ALLOWLIST: tuple[str, ...] = ()
BASELINE_PROMPT_INPUT_READ_RE = re.compile(
    r"^test/(?P<iteration>(?:iteration-\d+|.+-test\d+))/(?P<skill>[^/_][^/]*)/eval-\d+/input/(?:prompt\.md|prompt\.json)$"
)
WITH_SKILL_PROMPT_INPUT_READ_RE = re.compile(
    r"^test/(?P<iteration>(?:iteration-\d+|.+-test\d+))/(?P<skill>[^/_][^/]*)/eval-\d+/input/(?:prompt\.md|prompt\.json)$"
)
MANAGER_READ_ALLOWLIST = (
    "README.md",
    "test/",
    ".github/agents/",
    ".github/skills/",
    ".github/copilot-instructions.md",
)
MANAGER_EDIT_ALLOWLIST = (
    "README.md",
    "test/",
    ".github/agents/",
)
MANAGER_EDIT_DENY_PREFIXES = (
    ".github/agents/scripts/",
)
WORKER_WRITE_MODES = {
    "baseline",
    "baseline_hook_only",
    "with_skill_targeted",
}
WORKER_WRITE_PREFIX = "test/"
WORKER_WRITE_DENY_PREFIXES = (
    "test/scripts/",
    "test/_agent-hooks/",
    "test/_meta/",
)
BLIND_COMPARE_RAW_JOURNAL_RE = re.compile(
    r"^test/(?P<iteration>(?:iteration-\d+|.+-test\d+))/_meta/raw-comparison-[^/]+\.json$"
)
ALLOWED_MANAGER_COMMANDS = (
    re.compile(r"^(python|python3|py(?:\s+-3)?)\s+test/scripts/skill_suite_tools\.py\b"),
    re.compile(r"^(python|python3|py(?:\s+-3)?)\s+\.github/agents/scripts/enforce-test-access\.py\b"),
    re.compile(r"^(python|python3|py(?:\s+-3)?)\s+-m\s+pytest\b.*\btest/scripts/"),
    re.compile(r"^pytest\b.*\btest/scripts/"),
    re.compile(r"^git(?:\s+--no-pager)?\s+(status|diff)\b"),
)
PATHISH_KEYS = {
    "filepath",
    "filepaths",
    "path",
    "paths",
    "dirpath",
    "uri",
    "includepattern",
    "query",
    "old_path",
    "new_path",
}
COMMAND_KEYS = {"command", "args"}
COMMAND_ITERATION_ARG_RE = re.compile(r"--iteration(?:=|\s+)(\"[^\"]+\"|'[^']+'|[^\s]+)")
COMMAND_TEST_ITERATION_RE = re.compile(r"test[\\/](iteration-\d+|[^\\/\s\"']+-test\d+)(?:[\\/]|$)")
SKILL_SUITE_SUBCOMMAND_RE = re.compile(r"skill_suite_tools\.py\s+([a-z0-9-]+)")
ITERATION_REQUIRED_MANAGER_SUBCOMMANDS = {
    "aggregate",
    "clean-benchmark-artifacts",
    "materialize-comparisons",
    "materialize-comparisons-stdin",
    "resume-finalize",
    "write-run-metrics",
    "write-run-metrics-auto",
    "summarize-phase",
    "summarize-config",
    "prepare-blind",
    "protocol-preflight",
    "synthesis-bundle",
    "write-synthesis",
}
MANAGER_SUBCOMMAND_REQUIRED_FLAGS: dict[str, tuple[str, ...]] = {
    "summarize-config": ("--config",),
    "summarize-phase": ("--config",),
    "write-run-metrics": ("--started-at", "--finished-at", "--files-read-count", "--files-written-count"),
}
STATE_FILENAME_RE = re.compile(r"[^A-Za-z0-9_.-]+")


def main() -> None:
    try:
        raw = sys.stdin.read().strip()
        payload = json.loads(raw) if raw else {}
        event_name = infer_hook_event_name(payload)
        mode = os.environ.get("BENCH_MODE", "").strip()

        maybe_write_debug(payload, mode)

        if event_name == "SessionStart":
            emit(session_start_output(mode))
            return
        if event_name == "SubagentStart":
            emit(subagent_start_output(mode))
            return
        if event_name != "PreToolUse":
            emit(common_allow())
            return

        emit(handle_pre_tool_use(payload, mode))
    except Exception as exc:  # pragma: no cover - safety belt for hook runtime
        print(f"benchmark hook failure: {exc}", file=sys.stderr)
        raise SystemExit(2)


def emit(data: dict[str, Any]) -> None:
    print(json.dumps(data, ensure_ascii=False))


def infer_hook_event_name(payload: dict[str, Any]) -> str:
    direct = payload.get("hookEventName") or payload.get("hook_event_name")
    if isinstance(direct, str) and direct.strip():
        return direct.strip()
    if payload.get("tool_name"):
        return "PreToolUse"
    return ""


def maybe_write_debug(payload: dict[str, Any], mode: str) -> None:
    enabled = os.environ.get("BENCH_DEBUG_HOOKS", "").strip().lower()
    if enabled not in {"1", "true", "yes", "on"}:
        return
    log_target = os.environ.get("BENCH_DEBUG_LOG", "").strip()
    if not log_target:
        return

    cwd = payload.get("cwd") or "."
    try:
        workspace_root = Path(cwd).resolve()
    except Exception:
        workspace_root = Path(".").resolve()

    log_path = Path(log_target)
    if not log_path.is_absolute():
        log_path = workspace_root / log_target
    log_path.parent.mkdir(parents=True, exist_ok=True)

    tool_name = str(payload.get("tool_name", ""))
    tool_input = payload.get("tool_input") if isinstance(payload, dict) else None
    record = {
        "timestamp": payload.get("timestamp"),
        "hookEventName": payload.get("hookEventName"),
        "mode": mode,
        "sessionId": payload.get("sessionId"),
        "tool_name": tool_name,
        "tool_paths": extract_paths(tool_name, tool_input, workspace_root) if tool_input is not None else [],
    }
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def common_allow() -> dict[str, Any]:
    return {"continue": True}


def session_start_output(mode: str) -> dict[str, Any]:
    messages = {
        "benchmark_manager": (
            "Benchmark manager mode is active. Use the workspace skill 'skill-creator' "
            "when revising benchmark customizations, and delegate "
            "only to the constrained benchmark worker agents. MCP tools remain disabled in this mode."
        ),
        "baseline": (
            "Strict baseline benchmark worker mode is active. Workspace skills must have been "
            "relocated out of .github/skills/ before the session started, and no SKILL.md file "
            "may be read in this session. Outside the target prompt and benchmark artefacts, "
            "no project folders may be read. LikeC4 MCP use "
            "must stay limited to narrow element/relationship grounding; project listing, project "
            "summaries, and view browsing remain blocked. Other MCP servers remain blocked."
        ),
        "baseline_hook_only": (
            "Hook-only baseline probe mode is active. Workspace skills may remain in place, "
            "but no .github path or SKILL.md file may be read in this session. Outside the "
            "target prompt and benchmark artefacts, no project folders may be read. "
            "LikeC4 MCP use must stay limited to narrow "
            "element/relationship grounding; project listing, project summaries, and view browsing "
            "remain blocked. All other MCP servers remain blocked. Treat this as an experiment, not "
            "the default trust boundary."
        ),
        "with_skill_targeted": (
            "Targeted with-skill worker mode is active. The first skill directory you read "
            "becomes the only workspace skill allowed for the rest of the session. Outside that "
            "skill, no project folders may be read. "
            "Within the target skill, read eval prompts only from evals/evals-public.json; "
            "grading-spec.json stays hidden from workers. LikeC4 MCP use must stay limited to narrow "
            "element/relationship grounding; project listing, project summaries, and view browsing "
            "remain blocked. All other MCP servers remain blocked."
        ),
        "blind_compare": (
            "Blind comparator mode is active. Stay blind to mapping and raw non-blind outputs; "
            "read only blind A/B artifacts from the active iteration plus the target grading-spec.json. "
            "When the orchestrator provides an explicit raw_output_path, you may journal the raw comparator "
            "payload only under test/<iteration>/_meta/raw-comparison-*.json. MCP tools remain blocked in this mode."
        ),
    }
    additional = messages.get(mode)
    if not additional:
        return common_allow()
    return {
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": additional,
        }
    }


def subagent_start_output(mode: str) -> dict[str, Any]:
    if mode != "benchmark_manager":
        return common_allow()
    return {
        "hookSpecificOutput": {
            "hookEventName": "SubagentStart",
            "additionalContext": (
                "You were launched by the benchmark manager. Your own scoped hooks must remain "
                "the source of truth for file access. Do not spawn further subagents unless an "
                "equal-or-stricter hook policy exists for them."
            ),
        }
    }


def handle_pre_tool_use(payload: dict[str, Any], mode: str) -> dict[str, Any]:
    tool_name = str(payload.get("tool_name", ""))
    tool_input = payload.get("tool_input", {})
    workspace_root = Path(payload.get("cwd") or ".").resolve()
    state = load_state(workspace_root, payload.get("sessionId", "default"), mode)

    baseline_precondition_failure = strict_baseline_precondition_failure(mode, workspace_root)
    if baseline_precondition_failure:
        return deny(baseline_precondition_failure)

    if tool_name.startswith("mcp_"):
        if is_allowed_likec4_mcp(tool_name, mode):
            return allow(
                additional_context=(
                    "LikeC4 MCP is allowed in this benchmark worker for repository grounding and "
                    "validation. Manager and blind-comparator modes still keep MCP disabled."
                )
            )
        return deny(
            "MCP tools are disabled in this benchmark mode. Only LikeC4 MCP tools "
            "(mcp_likec4_*) are allowed in baseline, hook-only baseline, and with-skill workers."
        )

    category = classify_tool(tool_name)

    if category == "web":
        return deny("Web access is out of scope for benchmark agents.")
    if category == "semantic_search":
        return deny("semantic_search is denied because it cannot be scoped tightly enough for benchmark isolation.")
    if category == "agent":
        return handle_agent_invocation(tool_input, mode)
    if category == "execute":
        return handle_execute(tool_input, workspace_root, mode, state)
    if category == "edit":
        return handle_edit(tool_name, tool_input, workspace_root, mode, state)
    if category == "search":
        return handle_search(tool_name, tool_input, workspace_root, mode, state)
    if category == "safe_meta":
        return allow()
    if category == "read":
        return handle_read(tool_name, tool_input, workspace_root, mode, state)

    return deny(f"Tool '{tool_name}' is not allowed in benchmark mode '{mode}'.")


def strict_baseline_precondition_failure(mode: str, workspace_root: Path) -> str | None:
    if mode != "baseline":
        return None

    skills_root = workspace_root / ".github" / "skills"
    if not skills_root.exists():
        return None

    active_skills = sorted(child.name for child in skills_root.iterdir() if child.is_dir())
    if not active_skills:
        return None

    preview = ", ".join(active_skills[:3])
    if len(active_skills) > 3:
        preview += f", … (+{len(active_skills) - 3} more)"

    return (
        "Strict baseline mode requires relocating workspace skills out of .github/skills/ "
        f"before the session starts. Active skill directories are still present ({preview}). "
        "Use the hook-only baseline worker only for explicit isolation probes."
    )


def normalize_tool_name(tool_name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", tool_name.lower())


def is_allowed_likec4_mcp(tool_name: str, mode: str) -> bool:
    if mode not in ALLOWED_LIKEC4_MCP_MODES:
        return False
    normalized = normalize_tool_name(tool_name)
    return normalized.startswith(ALLOWED_LIKEC4_MCP_PREFIX) and normalized != ALLOWED_LIKEC4_MCP_PREFIX


def classify_tool(tool_name: str) -> str:
    lowered = tool_name.lower()
    if tool_name in SAFE_META_TOOL_NAMES:
        return "safe_meta"
    if tool_name in AGENT_TOOL_NAMES or "subagent" in lowered:
        return "agent"
    if tool_name in EXECUTE_TOOL_NAMES or "terminal" in lowered or "task" in lowered:
        return "execute"
    if tool_name in EDIT_TOOL_NAMES or lowered.startswith("edit") or lowered.startswith("create_"):
        return "edit"
    if tool_name == "semantic_search":
        return "semantic_search"
    if tool_name in SEARCH_TOOL_NAMES or lowered.endswith("search"):
        return "search"
    if tool_name in WEB_TOOL_NAMES or lowered.startswith("fetch") or lowered.startswith("open_browser"):
        return "web"
    if tool_name in READ_ONLY_TOOL_NAMES or lowered.startswith("read") or lowered.endswith("summary"):
        return "read"
    return "unknown"


def handle_agent_invocation(tool_input: Any, mode: str) -> dict[str, Any]:
    if mode != "benchmark_manager":
        return deny("Benchmark worker agents may not spawn subagents; this avoids escaping their file-access policy.")

    allowed_agents = {
        name.strip()
        for name in os.environ.get("BENCH_ALLOWED_AGENTS", "").split(",")
        if name.strip()
    }
    requested_agent = extract_subagent_name(tool_input)
    if not requested_agent:
        return deny("Subagent invocation must specify an explicit benchmark agent name.")
    if requested_agent not in allowed_agents:
        return deny(
            f"Subagent '{requested_agent}' is not in the benchmark allowlist. Only constrained benchmark worker agents may be delegated to."
        )
    return allow(
        additional_context=(
            f"Delegation approved only because '{requested_agent}' is an explicitly allowlisted benchmark worker agent with its own scoped hook policy."
        )
    )


def extract_subagent_name(tool_input: Any) -> str | None:
    if isinstance(tool_input, dict):
        for key in ("agentName", "agent_name", "agent", "name"):
            value = tool_input.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()
    return None


def handle_execute(tool_input: Any, workspace_root: Path, mode: str, state: dict[str, Any]) -> dict[str, Any]:
    if mode != "benchmark_manager":
        return deny("Terminal and task execution are disabled for benchmark worker agents.")

    commands = extract_commands(tool_input)
    if not commands:
        return deny("Benchmark manager execution is limited to audited commands; no command was found in the tool payload.")

    for command in commands:
        normalized = " ".join(command.strip().split())
        normalized_candidates = normalize_manager_command_candidates(normalized)
        if not normalized_candidates:
            return deny(
                f"Command '{normalized}' is outside the benchmark-manager allowlist. Use test/scripts helpers, pytest under test/scripts, or harmless git inspection only."
            )
        for candidate in normalized_candidates:
            if not any(pattern.search(candidate) for pattern in ALLOWED_MANAGER_COMMANDS):
                return deny(
                    f"Command '{candidate}' is outside the benchmark-manager allowlist. Use test/scripts helpers, pytest under test/scripts, or harmless git inspection only."
                )

    iteration_candidates = extract_iteration_candidates_from_commands(commands, workspace_root)
    for command in commands:
        subcommand = extract_skill_suite_subcommand(command)
        if subcommand in ITERATION_REQUIRED_MANAGER_SUBCOMMANDS and not iteration_candidates:
            return deny(
                f"Command '{subcommand}' must provide an explicit --iteration test/<iteration> argument. "
                "Implicit/default iteration resolution is denied to avoid writing benchmark artifacts to the wrong folder."
            )
        required_flags = MANAGER_SUBCOMMAND_REQUIRED_FLAGS.get(subcommand or "")
        if required_flags:
            missing = [flag for flag in required_flags if not has_command_flag(command, flag)]
            if missing:
                return deny(
                    f"Command '{subcommand}' is missing required flag(s): {', '.join(missing)}. "
                    "Provide explicit arguments to keep benchmark runs deterministic and resumable."
                )

    iteration_scope_failure = enforce_iteration_scope(state, workspace_root, iteration_candidates, mode)
    if iteration_scope_failure:
        return deny(iteration_scope_failure)
    return allow()


def extract_commands(tool_input: Any) -> list[str]:
    commands: list[str] = []
    if isinstance(tool_input, dict):
        for key, value in tool_input.items():
            lowered = key.lower()
            if lowered in COMMAND_KEYS:
                if isinstance(value, str):
                    commands.append(value)
                elif isinstance(value, list):
                    commands.extend(str(item) for item in value if isinstance(item, (str, int, float)))
            else:
                commands.extend(extract_commands(value))
    elif isinstance(tool_input, list):
        for item in tool_input:
            commands.extend(extract_commands(item))
    return commands


def normalize_manager_command_candidates(command: str) -> list[str]:
    stripped = command.strip()
    if not stripped:
        return []

    # Keep manager execution deterministic and avoid shell escape patterns.
    if any(token in stripped for token in ("|", ">", "<", "$(", "`") ):
        return []

    if re.match(r"^for\b", stripped):
        loop_match = re.search(r"\bdo\b(?P<body>.*)\bdone\b", stripped)
        if not loop_match:
            return []
        body = loop_match.group("body")
        return [segment for segment in split_manager_command_segments(body) if segment]

    return [segment for segment in split_manager_command_segments(stripped) if segment]


def split_manager_command_segments(command: str) -> list[str]:
    segments = [segment.strip() for segment in re.split(r"&&|;|\n", command) if segment.strip()]
    filtered: list[str] = []
    for segment in segments:
        lowered = segment.lower()
        if lowered in {"do", "done", "then", "fi"}:
            continue
        filtered.append(" ".join(segment.split()))
    return filtered


def has_command_flag(command: str, flag: str) -> bool:
    escaped = re.escape(flag)
    return bool(re.search(rf"(?:^|\s){escaped}(?:\s+[^\s]+|=[^\s]+)?(?:\s|$)", command))


def extract_skill_suite_subcommand(command: str) -> str | None:
    match = SKILL_SUITE_SUBCOMMAND_RE.search(command)
    if not match:
        return None
    return match.group(1)


def unquote_token(value: str) -> str:
    if len(value) >= 2 and ((value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'"))):
        return value[1:-1]
    return value


def extract_iteration_candidates_from_commands(commands: list[str], workspace_root: Path) -> set[str]:
    iterations: set[str] = set()
    for command in commands:
        for match in COMMAND_ITERATION_ARG_RE.finditer(command):
            raw_value = unquote_token(match.group(1).strip())
            rel_path = normalize_to_repo_relative(raw_value, workspace_root)
            if rel_path:
                iteration_name = extract_iteration_from_iteration_path(rel_path)
                if iteration_name:
                    iterations.add(iteration_name)
        for match in COMMAND_TEST_ITERATION_RE.finditer(command):
            iteration_name = match.group(1)
            if is_benchmark_iteration_dir(iteration_name):
                iterations.add(iteration_name)
    return iterations


def handle_edit(
    tool_name: str,
    tool_input: Any,
    workspace_root: Path,
    mode: str,
    state: dict[str, Any],
) -> dict[str, Any]:
    if mode == "blind_compare":
        paths = extract_paths(tool_name, tool_input, workspace_root)
        if not paths:
            return deny("Could not determine which files would be edited; blind comparator writes must be explicitly path-scoped.")

        for rel_path in paths:
            if not is_blind_compare_write_allowed(rel_path):
                return deny(
                    f"Editing '{rel_path}' is outside the blind comparator write scope. Blind comparator workers may only write raw-comparison journal files under test/<iteration>/_meta/."
                )

        iteration_scope_failure = enforce_iteration_scope(
            state,
            workspace_root,
            extract_iteration_candidates_from_paths(paths),
            mode,
        )
        if iteration_scope_failure:
            return deny(iteration_scope_failure)

        return allow(
            additional_context="Blind comparator write allowed only for raw-comparison journal files under test/<iteration>/_meta/."
        )

    if mode not in {"benchmark_manager"} and mode not in WORKER_WRITE_MODES:
        return deny("Editing tools are disabled for benchmark worker agents.")

    paths = extract_paths(tool_name, tool_input, workspace_root)
    if not paths:
        return deny("Could not determine which files would be edited; benchmark edits must be explicitly path-scoped.")

    if mode == "benchmark_manager":
        for rel_path in paths:
            if not is_manager_edit_allowed(rel_path):
                return deny(
                    f"Editing '{rel_path}' is outside the benchmark-manager allowlist. Only README.md, test/, and .github/agents/*.agent.md are editable from this agent."
                )

        iteration_scope_failure = enforce_iteration_scope(
            state,
            workspace_root,
            extract_iteration_candidates_from_paths(paths),
            mode,
        )
        if iteration_scope_failure:
            return deny(iteration_scope_failure)
        return allow()

    for rel_path in paths:
        if not is_worker_write_allowed(rel_path):
            return deny(
                f"Editing '{rel_path}' is outside the worker write scope. Workers may only write under test/<iteration>/<skill>/ directories."
            )

    iteration_scope_failure = enforce_iteration_scope(
        state,
        workspace_root,
        extract_iteration_candidates_from_paths(paths),
        mode,
    )
    if iteration_scope_failure:
        return deny(iteration_scope_failure)

    return allow(
        additional_context="Worker write allowed under test/ iteration scope for response materialization."
    )


def handle_search(
    tool_name: str,
    tool_input: Any,
    workspace_root: Path,
    mode: str,
    state: dict[str, Any],
) -> dict[str, Any]:
    if tool_name == "semantic_search":
        return deny("semantic_search is denied because it searches the whole workspace without a reliable file-scope fence.")

    include_patterns = extract_search_scopes(tool_input)
    if not include_patterns:
        return deny("Search tools must be scoped to an allowed path prefix; unscoped workspace search is denied for benchmark isolation.")

    for pattern in include_patterns:
        prefix = normalize_glob_prefix(pattern)
        if prefix is None:
            return deny(
                f"Search scope '{pattern}' is too broad. Scope searches to a concrete allowed subtree "
                "that is explicitly permitted for the current benchmark mode."
            )
        if not is_read_allowed(prefix, mode, state, workspace_root, is_prefix=True):
            return deny(f"Search scope '{pattern}' is outside the allowed benchmark area for mode '{mode}'.")
    return allow()


def extract_search_scopes(tool_input: Any) -> list[str]:
    scopes: list[str] = []
    if isinstance(tool_input, dict):
        include_pattern = tool_input.get("includePattern")
        if isinstance(include_pattern, str) and include_pattern.strip():
            scopes.append(include_pattern.strip())
        query = tool_input.get("query")
        if isinstance(query, str) and looks_like_pathish_glob(query):
            scopes.append(query.strip())
    return scopes


def handle_read(
    tool_name: str,
    tool_input: Any,
    workspace_root: Path,
    mode: str,
    state: dict[str, Any],
) -> dict[str, Any]:
    paths = extract_paths(tool_name, tool_input, workspace_root)
    if not paths:
        return allow()

    for rel_path in paths:
        if not is_read_allowed(rel_path, mode, state, workspace_root):
            return deny(f"Reading '{rel_path}' is denied in benchmark mode '{mode}'.")
    return allow()


def is_manager_edit_allowed(rel_path: str) -> bool:
    if any(rel_path.startswith(prefix) for prefix in MANAGER_EDIT_DENY_PREFIXES):
        return False
    if rel_path == "README.md":
        return True
    if rel_path.startswith("test/"):
        return True
    if rel_path.startswith(".github/agents/") and rel_path.endswith(".agent.md"):
        return True
    return False


def is_worker_write_allowed(rel_path: str) -> bool:
    if not rel_path.startswith(WORKER_WRITE_PREFIX):
        return False
    if any(rel_path.startswith(prefix) for prefix in WORKER_WRITE_DENY_PREFIXES):
        return False
    parts = rel_path.split("/")
    if len(parts) < 3:
        return False
    iteration_name = parts[1]
    if not is_benchmark_iteration_dir(iteration_name):
        return False
    if len(parts) >= 3 and parts[2].startswith("_"):
        return False
    return True


def is_blind_compare_write_allowed(rel_path: str) -> bool:
    normalized = normalize_rel_path(rel_path)
    match = BLIND_COMPARE_RAW_JOURNAL_RE.match(normalized)
    if not match:
        return False
    iteration_name = match.group("iteration")
    return is_benchmark_iteration_dir(iteration_name)


def configured_allowed_iteration() -> str | None:
    raw = os.environ.get("BENCH_ALLOWED_ITERATION", "").strip()
    if not raw:
        return None
    normalized = normalize_rel_path(raw)
    if normalized.startswith("test/"):
        parts = normalized.split("/")
        if len(parts) >= 2:
            normalized = parts[1]
    if not is_benchmark_iteration_dir(normalized):
        return None
    return normalized


def extract_iteration_candidates_from_paths(paths: list[str]) -> set[str]:
    iterations: set[str] = set()
    for rel_path in paths:
        iteration_name = extract_iteration_from_iteration_path(rel_path)
        if iteration_name:
            iterations.add(iteration_name)
    return iterations


def enforce_iteration_scope(
    state: dict[str, Any],
    workspace_root: Path,
    iteration_candidates: set[str],
    mode: str,
) -> str | None:
    if not iteration_candidates:
        return None

    configured_iteration = configured_allowed_iteration()
    if configured_iteration:
        unexpected = sorted(candidate for candidate in iteration_candidates if candidate != configured_iteration)
        if unexpected:
            return (
                f"Writes/commands target iteration(s) {', '.join(unexpected)} but BENCH_ALLOWED_ITERATION is locked to '{configured_iteration}'."
            )

    if len(iteration_candidates) > 1:
        return (
            "A single tool call may not target multiple benchmark iterations. "
            f"Found: {', '.join(sorted(iteration_candidates))}."
        )

    requested = next(iter(iteration_candidates))
    locked = state.get("locked_iteration")
    if locked and locked != requested:
        return (
            f"Iteration scope is locked to '{locked}' for this session, but this operation targets '{requested}'. "
            "Start a fresh session to switch iteration targets."
        )

    if configured_iteration and requested != configured_iteration:
        return (
            f"Iteration '{requested}' is denied because BENCH_ALLOWED_ITERATION is '{configured_iteration}'."
        )

    if not locked:
        state["locked_iteration"] = requested
        save_state(workspace_root, state)

    if mode == "benchmark_manager":
        return None

    return None


def is_read_allowed(
    rel_path: str,
    mode: str,
    state: dict[str, Any],
    workspace_root: Path,
    *,
    is_prefix: bool = False,
) -> bool:
    rel_path = normalize_rel_path(rel_path)
    if not rel_path:
        return False

    if any(rel_path.startswith(prefix) for prefix in FORBIDDEN_NON_WORKER_PREFIXES):
        return False

    if rel_path.startswith(EXTERNAL_PATH_TAG):
        return False

    if "/_disabled-skills/" in f"/{rel_path}":
        return False

    if mode == "benchmark_manager":
        return any(path_matches_allowlist(rel_path, allowed, is_prefix=is_prefix) for allowed in MANAGER_READ_ALLOWLIST)

    if mode in {"baseline", "baseline_hook_only"}:
        if rel_path.startswith(".github/"):
            return False
        if is_baseline_prompt_input_read_allowed(rel_path, state, workspace_root):
            return True
        return any(path_matches_allowlist(rel_path, allowed, is_prefix=is_prefix) for allowed in ROOT_READ_ALLOWLIST)

    if mode == "with_skill_targeted":
        if is_with_skill_prompt_input_read_allowed(rel_path, state, workspace_root):
            return True
        if rel_path.startswith(".github/skills/"):
            skill_name = extract_skill_from_skills_path(rel_path)
            if not skill_name:
                return False
            if not lock_skill(state, skill_name, workspace_root):
                return False
            locked_skill = state.get("locked_skill")
            if skill_name != locked_skill:
                return False
            if "/evals/" in rel_path:
                return rel_path.endswith("/evals/evals-public.json")
            return True
        return any(path_matches_allowlist(rel_path, allowed, is_prefix=is_prefix) for allowed in ROOT_READ_ALLOWLIST)

    if mode == "blind_compare":
        if rel_path.endswith("blind-map.json"):
            return False
        if "/with_skill/" in f"/{rel_path}" or "/without_skill/" in f"/{rel_path}":
            return False
        if rel_path.endswith("SKILL.md"):
            return False
        if rel_path.endswith("-summary.json") or rel_path.endswith("-run-metrics.json"):
            return False
        if rel_path.endswith("blind-comparisons.json"):
            return False
        if rel_path.startswith(".github/skills/"):
            if not rel_path.endswith("/evals/grading-spec.json"):
                return False
            skill_name = extract_skill_from_skills_path(rel_path)
            if not skill_name:
                return False
            if not lock_skill(state, skill_name, workspace_root):
                return False
            return skill_name == state.get("locked_skill")
        blind_artifact_path = (
            rel_path.endswith("/blind/A.md")
            or rel_path.endswith("/blind/B.md")
            or re.search(r"/blind/run-\d+/(A|B)\.md$", rel_path)
        )
        blind_directory_prefix = is_prefix and bool(re.search(r"/blind(?:/run-\d+)?/?$", rel_path))
        if blind_artifact_path or blind_directory_prefix:
            skill_name = extract_skill_from_iteration_path(rel_path)
            iteration_name = extract_iteration_from_iteration_path(rel_path)
            current_iteration = latest_iteration_name(workspace_root)
            if not skill_name or not iteration_name or not current_iteration:
                return False
            if iteration_name != current_iteration:
                return False
            if not lock_skill(state, skill_name, workspace_root):
                return False
            if not lock_iteration(state, iteration_name, workspace_root):
                return False
            return skill_name == state.get("locked_skill")
        return False

    return False


def is_baseline_prompt_input_read_allowed(rel_path: str, state: dict[str, Any], workspace_root: Path) -> bool:
    match = BASELINE_PROMPT_INPUT_READ_RE.match(rel_path)
    if not match:
        return False
    iteration_name = match.group("iteration")
    return lock_iteration(state, iteration_name, workspace_root)


def is_with_skill_prompt_input_read_allowed(rel_path: str, state: dict[str, Any], workspace_root: Path) -> bool:
    match = WITH_SKILL_PROMPT_INPUT_READ_RE.match(rel_path)
    if not match:
        return False
    iteration_name = match.group("iteration")
    skill_name = match.group("skill")
    if not lock_iteration(state, iteration_name, workspace_root):
        return False
    if not lock_skill(state, skill_name, workspace_root):
        return False
    return state.get("locked_skill") == skill_name


def path_matches_allowlist(rel_path: str, allowed: str, *, is_prefix: bool) -> bool:
    if allowed.endswith("/"):
        return rel_path.startswith(allowed) or (is_prefix and allowed.startswith(rel_path))
    return rel_path == allowed or (is_prefix and rel_path.startswith(allowed))


def lock_skill(state: dict[str, Any], skill_name: str, workspace_root: Path) -> bool:
    existing = state.get("locked_skill")
    if existing and existing != skill_name:
        return False
    if not existing:
        state["locked_skill"] = skill_name
        save_state(workspace_root, state)
    return True


def lock_iteration(state: dict[str, Any], iteration_name: str, workspace_root: Path) -> bool:
    existing = state.get("locked_iteration")
    if existing and existing != iteration_name:
        return False
    if not existing:
        state["locked_iteration"] = iteration_name
        save_state(workspace_root, state)
    return True


def load_state(workspace_root: Path, session_id: str, mode: str) -> dict[str, Any]:
    path = state_path(workspace_root, session_id)
    if path.exists():
        data = json.loads(path.read_text(encoding="utf-8"))
        if data.get("mode") == mode:
            return data
    return {"mode": mode, "session_id": session_id}


def save_state(workspace_root: Path, state: dict[str, Any]) -> None:
    path = state_path(workspace_root, state.get("session_id", "default"))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def state_path(workspace_root: Path, session_id: str) -> Path:
    state_root = os.environ.get("BENCH_STATE_ROOT")
    base = Path(state_root).resolve() if state_root else (workspace_root / "test" / "_agent-hooks")
    safe_name = STATE_FILENAME_RE.sub("_", session_id or "default")
    return base / f"{safe_name}.json"


def extract_paths(tool_name: str, tool_input: Any, workspace_root: Path) -> list[str]:
    if tool_name == "apply_patch" and isinstance(tool_input, dict):
        patch_input = tool_input.get("input")
        if isinstance(patch_input, str):
            return [path for path in (normalize_to_repo_relative(value, workspace_root) for value in extract_patch_paths(patch_input)) if path]

    raw_values = collect_path_like_values(tool_input)
    normalized: list[str] = []
    for value in raw_values:
        rel = normalize_to_repo_relative(value, workspace_root)
        if rel:
            normalized.append(rel)
    return dedupe(normalized)


def collect_path_like_values(obj: Any, parent_key: str = "") -> list[str]:
    values: list[str] = []
    if isinstance(obj, dict):
        for key, value in obj.items():
            key_lower = key.lower()
            if isinstance(value, str) and (key_lower in PATHISH_KEYS or looks_like_pathish_glob(value)):
                values.append(value)
            else:
                values.extend(collect_path_like_values(value, key_lower))
    elif isinstance(obj, list):
        for item in obj:
            values.extend(collect_path_like_values(item, parent_key))
    elif isinstance(obj, str) and parent_key in PATHISH_KEYS:
        values.append(obj)
    return values


def extract_patch_paths(patch_input: str) -> list[str]:
    paths: list[str] = []
    for match in PATCH_PATH_RE.finditer(patch_input):
        value = match.group(1).strip()
        if " -> " in value:
            value = value.split(" -> ", 1)[0].strip()
        paths.append(value)
    return paths


def normalize_to_repo_relative(value: str, workspace_root: Path) -> str | None:
    candidate = value.strip().strip('"').strip("'")
    if not candidate:
        return None
    if candidate.startswith("http://") or candidate.startswith("https://"):
        return None

    if candidate.startswith("file://"):
        parsed = urlparse(candidate)
        candidate = unquote(parsed.path)
        if re.match(r"^/[A-Za-z]:/", candidate):
            candidate = candidate[1:]

    path = Path(candidate)
    if not path.is_absolute():
        path = (workspace_root / path).resolve()
    else:
        path = path.resolve()

    try:
        return normalize_rel_path(path.relative_to(workspace_root).as_posix())
    except ValueError:
        return f"{EXTERNAL_PATH_TAG}{path.as_posix()}"


def normalize_rel_path(value: str) -> str:
    normalized = value.replace("\\", "/")
    while normalized.startswith("./"):
        normalized = normalized[2:]
    return normalized.lstrip("/")


def is_benchmark_iteration_dir(name: str) -> bool:
    return bool(ITERATION_RE.match(name) or SERIES_ITERATION_RE.match(name))


def normalize_glob_prefix(pattern: str) -> str | None:
    cleaned = normalize_rel_path(pattern.strip())
    if not cleaned:
        return None
    if cleaned == "README.md":
        return cleaned
    if cleaned.startswith("**"):
        return None
    wildcard = WILDCARD_RE.search(cleaned)
    prefix = cleaned if wildcard is None else cleaned[: wildcard.start()]
    prefix = prefix.rstrip("/")
    if not prefix:
        return None
    if "/" in prefix:
        return prefix + "/" if not prefix.endswith("/") and not prefix.endswith(".md") and not prefix.endswith(".json") else prefix
    if prefix in {"projects", "test", ".github"}:
        return prefix + "/"
    return prefix


def looks_like_pathish_glob(value: str) -> bool:
    stripped = value.strip()
    if not stripped:
        return False
    if stripped.startswith("http://") or stripped.startswith("https://"):
        return False
    return "/" in stripped or "\\" in stripped or stripped.endswith((".md", ".json", ".py", ".ipynb"))


def extract_skill_from_skills_path(rel_path: str) -> str | None:
    parts = normalize_rel_path(rel_path).split("/")
    if len(parts) >= 3 and parts[0] == ".github" and parts[1] == "skills":
        return parts[2]
    return None


def extract_skill_from_iteration_path(rel_path: str) -> str | None:
    parts = normalize_rel_path(rel_path).split("/")
    if len(parts) >= 3 and parts[0] == "test" and is_benchmark_iteration_dir(parts[1]):
        candidate = parts[2]
        if candidate.startswith("_") or candidate == "scripts":
            return None
        return candidate
    return None


def extract_iteration_from_iteration_path(rel_path: str) -> str | None:
    parts = normalize_rel_path(rel_path).split("/")
    if len(parts) >= 2 and parts[0] == "test" and is_benchmark_iteration_dir(parts[1]):
        return parts[1]
    return None


def latest_iteration_name(workspace_root: Path) -> str | None:
    test_root = workspace_root / "test"
    if not test_root.exists():
        return None
    candidates: list[tuple[int, str]] = []
    skill_series_candidates: list[tuple[int, str]] = []
    for child in test_root.iterdir():
        if not child.is_dir():
            continue
        if ITERATION_RE.match(child.name):
            try:
                number = int(child.name.split("-", 1)[1])
            except (IndexError, ValueError):
                continue
            candidates.append((number, child.name))
            continue
        if SERIES_ITERATION_RE.match(child.name):
            series_number = re.search(r"(\d+)$", child.name)
            if not series_number:
                continue
            skill_series_candidates.append((int(series_number.group(1)), child.name))
    if not candidates:
        if not skill_series_candidates:
            return None
        skill_series_candidates.sort()
        return skill_series_candidates[-1][1]
    candidates.sort()
    return candidates[-1][1]


def dedupe(values: list[str]) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for value in values:
        if value not in seen:
            seen.add(value)
            result.append(value)
    return result


def allow(*, additional_context: str | None = None) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "allow",
            "permissionDecisionReason": "Allowed by benchmark access policy.",
        }
    }
    if additional_context:
        payload["hookSpecificOutput"]["additionalContext"] = additional_context
    return payload


def deny(reason: str) -> dict[str, Any]:
    return {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }
    }


if __name__ == "__main__":
    main()
