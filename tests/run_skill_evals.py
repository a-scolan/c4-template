#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import statistics
import subprocess
import sys
import tempfile
import textwrap
import unicodedata
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PRIMARY_CONFIG = "with_skill"
CONFIG_ORDER = ["with_skill", "old_skill", "without_skill"]
DEFAULT_MODEL = "gpt-5.4"
DEFAULT_TIMEOUT_SECONDS = 300
DEFAULT_WITHOUT_SKILL_MODE = "target-only"
DEFAULT_MCP_CONFIG = Path.home() / ".vscode" / "mcp.json"

IGNORED_TOP_LEVEL_NAMES = {
    ".git",
    ".pytest_cache",
    "__pycache__",
    "node_modules",
}

IGNORED_FILE_SUFFIXES = {
    ".pyc",
    ".pyo",
}

IGNORED_DIFF_PREFIXES = [
    Path("Microsoft") / "Windows" / "PowerShell",
]


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def parse_args() -> argparse.Namespace:
    repo_root_default = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(
        description="Run GitHub Copilot CLI skill evaluations in isolated sandboxes.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "skill_name",
        help="Repository-local skill name under .github/skills/<skill-name>/, or `all` to process every skill with evals",
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=repo_root_default,
        help="Repository root containing .github/skills and tests/skills",
    )
    parser.add_argument(
        "--workspace-root",
        type=Path,
        default=repo_root_default / "tests" / "skills",
        help="Directory where evaluation workspaces are persisted. Must live outside .github/skills",
    )
    parser.add_argument(
        "--configs",
        nargs="+",
        choices=CONFIG_ORDER,
        help="Configurations to run. Defaults to with_skill + old_skill if a snapshot exists, else with_skill + without_skill.",
    )
    parser.add_argument(
        "--eval-ids",
        nargs="+",
        type=int,
        help="Subset of eval IDs from evals.json to execute",
    )
    parser.add_argument(
        "--runs-per-configuration",
        type=int,
        default=1,
        help="How many repeated runs to execute per eval/configuration",
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help="Copilot CLI model name used for executor and grader runs",
    )
    parser.add_argument(
        "--timeout-seconds",
        type=int,
        default=DEFAULT_TIMEOUT_SECONDS,
        help="Timeout for each executor or grader Copilot CLI call",
    )
    parser.add_argument(
        "--force-iteration",
        type=int,
        help="Force the iteration number instead of auto-incrementing",
    )
    parser.add_argument(
        "--mcp-config",
        type=Path,
        default=DEFAULT_MCP_CONFIG,
        help="VS Code MCP config file to re-inject into isolated runs",
    )
    parser.add_argument(
        "--no-mcp",
        action="store_true",
        help="Do not add extra MCP config from VS Code to isolated runs",
    )
    parser.add_argument(
        "--skip-grading",
        action="store_true",
        help="Skip the grader pass and emit placeholder grading.json files",
    )
    parser.add_argument(
        "--report-only",
        action="store_true",
        help="Do not execute Copilot runs; only regenerate workspace history and global overview reports from existing benchmarks",
    )
    parser.add_argument(
        "--without-skill-mode",
        choices=["target-only", "no-repo-skills"],
        default=DEFAULT_WITHOUT_SKILL_MODE,
        help="How strictly to disable repository-local skills for without_skill runs",
    )
    return parser.parse_args()


def log(message: str) -> None:
    print(message, flush=True)


def load_json_file(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json_file(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def slugify(text: str, max_length: int = 48) -> str:
    normalized = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    normalized = normalized.lower()
    normalized = re.sub(r"[^a-z0-9]+", "-", normalized)
    normalized = re.sub(r"-{2,}", "-", normalized).strip("-")
    if not normalized:
        return "eval"
    return normalized[:max_length].rstrip("-") or "eval"


def iteration_key(path: Path) -> int:
    match = re.match(r"iteration-(\d+)$", path.name)
    return int(match.group(1)) if match else -1


def determine_iteration(workspace_dir: Path, forced: int | None) -> int:
    if forced is not None:
        return forced
    existing = [iteration_key(path) for path in workspace_dir.glob("iteration-*") if path.is_dir()]
    return (max(existing) + 1) if existing else 1


def load_previous_eval_names(workspace_dir: Path) -> dict[int, str]:
    mapping: dict[int, str] = {}
    iterations = sorted((path for path in workspace_dir.glob("iteration-*") if path.is_dir()), key=iteration_key, reverse=True)
    for iteration_dir in iterations:
        for eval_dir in sorted(path for path in iteration_dir.iterdir() if path.is_dir()):
            metadata_path = eval_dir / "eval_metadata.json"
            if not metadata_path.exists():
                continue
            data = load_json_file(metadata_path)
            eval_id = data.get("eval_id")
            eval_name = data.get("eval_name")
            if isinstance(eval_id, int) and isinstance(eval_name, str) and eval_id not in mapping:
                mapping[eval_id] = eval_name
    return mapping


def derive_eval_name(eval_def: dict[str, Any], previous_names: dict[int, str]) -> str:
    eval_id = int(eval_def["id"])
    if eval_id in previous_names:
        return previous_names[eval_id]
    for key in ("eval_name", "name"):
        if key in eval_def and isinstance(eval_def[key], str) and eval_def[key].strip():
            return eval_def[key].strip()
    seed = str(eval_def.get("expected_output") or eval_def.get("prompt") or f"eval-{eval_id}")
    return f"eval-{slugify(seed)}"


def default_configs(snapshot_dir: Path) -> list[str]:
    if (snapshot_dir / "BASELINE_SKILL.md").exists():
        return ["with_skill", "old_skill"]
    return ["with_skill", "without_skill"]


def format_percent(value: float) -> str:
    return f"{value * 100:.1f}%"


def format_stat(mean: float, stddev: float, *, is_percent: bool = False) -> str:
    if is_percent:
        return f"{format_percent(mean)} ± {format_percent(stddev)}"
    return f"{mean:.2f} ± {stddev:.2f}"


def format_delta(value: float) -> str:
    sign = "+" if value >= 0 else ""
    return f"{sign}{value:.2f}"


def read_text_or_empty(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def strip_json_comments(text: str) -> str:
    result: list[str] = []
    i = 0
    in_string = False
    escape = False
    in_line_comment = False
    in_block_comment = False
    while i < len(text):
        char = text[i]
        next_char = text[i + 1] if i + 1 < len(text) else ""
        if in_line_comment:
            if char == "\n":
                in_line_comment = False
                result.append(char)
            i += 1
            continue
        if in_block_comment:
            if char == "*" and next_char == "/":
                in_block_comment = False
                i += 2
            else:
                i += 1
            continue
        if in_string:
            result.append(char)
            if escape:
                escape = False
            elif char == "\\":
                escape = True
            elif char == '"':
                in_string = False
            i += 1
            continue
        if char == '"':
            in_string = True
            result.append(char)
            i += 1
            continue
        if char == "/" and next_char == "/":
            in_line_comment = True
            i += 2
            continue
        if char == "/" and next_char == "*":
            in_block_comment = True
            i += 2
            continue
        result.append(char)
        i += 1
    return "".join(result).lstrip("\ufeff")


def try_insert_missing_comma(text: str, pos: int) -> str | None:
    insert_at = pos
    while insert_at < len(text) and text[insert_at].isspace():
        insert_at += 1
    if insert_at >= len(text):
        return None
    next_char = text[insert_at]
    prev_at = insert_at - 1
    while prev_at >= 0 and text[prev_at].isspace():
        prev_at -= 1
    if prev_at < 0:
        return None
    prev_char = text[prev_at]
    if next_char not in '"{[tfn-0123456789]':
        return None
    if prev_char in "{[,:":
        return None
    return text[:insert_at] + "," + text[insert_at:]


def try_remove_trailing_comma(text: str, pos: int) -> str | None:
    idx = pos - 1
    while idx >= 0 and text[idx].isspace():
        idx -= 1
    if idx >= 0 and text[idx] in "}]":
        comma_idx = idx - 1
        while comma_idx >= 0 and text[comma_idx].isspace():
            comma_idx -= 1
        if comma_idx >= 0 and text[comma_idx] == ",":
            return text[:comma_idx] + text[comma_idx + 1:]
    return None


def sanitize_json_text(text: str) -> tuple[dict[str, Any], str, list[str]]:
    cleaned = strip_json_comments(text)
    repairs: list[str] = []
    last_error: json.JSONDecodeError | None = None
    for _ in range(12):
        try:
            parsed = json.loads(cleaned)
            if not isinstance(parsed, dict):
                raise ValueError("Expected a JSON object at the root of the MCP config")
            return parsed, cleaned, repairs
        except json.JSONDecodeError as exc:
            last_error = exc
            inserted = try_insert_missing_comma(cleaned, exc.pos)
            if inserted is not None and inserted != cleaned:
                cleaned = inserted
                repairs.append(f"Inserted a missing comma near line {exc.lineno}, column {exc.colno}.")
                continue
            removed = try_remove_trailing_comma(cleaned, exc.pos)
            if removed is not None and removed != cleaned:
                cleaned = removed
                repairs.append(f"Removed a trailing comma near line {exc.lineno}, column {exc.colno}.")
                continue
            break
    if last_error is not None:
        raise ValueError(f"Unable to sanitize MCP config JSON: {last_error.msg} at line {last_error.lineno}, column {last_error.colno}.")
    raise ValueError("Unable to sanitize MCP config JSON.")


def ensure_command_available(command: str) -> None:
    if shutil.which(command):
        return
    raise SystemExit(f"Required command not found in PATH: {command}")


def build_isolated_env(temp_home: Path) -> dict[str, str]:
    env = dict(os.environ)
    temp_home_str = str(temp_home)
    env["HOME"] = temp_home_str
    env["USERPROFILE"] = temp_home_str
    env["COPILOT_HOME"] = str(temp_home / ".copilot")
    env["XDG_CONFIG_HOME"] = str(temp_home / ".config")
    env["GH_NO_UPDATE_NOTIFIER"] = "1"
    env["GIT_TERMINAL_PROMPT"] = "0"
    env.pop("COPILOT_SKILLS_DIRS", None)
    env.pop("COPILOT_CUSTOM_INSTRUCTIONS_DIRS", None)
    if os.name == "nt":
        drive, tail = os.path.splitdrive(temp_home_str)
        env["HOMEDRIVE"] = drive
        env["HOMEPATH"] = tail or "\\"
    return env


def prepare_isolated_home_fs(temp_home: Path) -> None:
    (temp_home / ".copilot").mkdir(parents=True, exist_ok=True)
    (temp_home / ".config").mkdir(parents=True, exist_ok=True)
    # Some Windows PowerShell profiles probe under USERPROFILE on startup.
    # Create the common path up front so isolated USERPROFILE values do not emit noise.
    (
        temp_home
        / "AppData"
        / "Roaming"
        / "Microsoft"
        / "Windows"
        / "PowerShell"
        / "PSReadLine"
    ).mkdir(parents=True, exist_ok=True)


def prepare_mcp_config(temp_home: Path, source_path: Path | None, *, enabled: bool) -> tuple[Path | None, list[str]]:
    notes: list[str] = []
    if not enabled:
        notes.append("MCP reinjection disabled via --no-mcp.")
        return None, notes
    if source_path is None:
        notes.append("No MCP config source provided.")
        return None, notes
    if not source_path.exists():
        notes.append(f"MCP config not found: {source_path}")
        return None, notes
    raw_text = source_path.read_text(encoding="utf-8", errors="replace")
    try:
        parsed, _, repairs = sanitize_json_text(raw_text)
    except ValueError as exc:
        notes.append(f"MCP config could not be sanitized and was skipped: {exc}")
        return None, notes
    if "servers" in parsed and "mcpServers" not in parsed:
        parsed = {**{key: value for key, value in parsed.items() if key != "servers"}, "mcpServers": parsed["servers"]}
        notes.append("Converted VS Code MCP root key `servers` to Copilot CLI key `mcpServers`.")
    if "mcpServers" not in parsed:
        notes.append("MCP config does not define `mcpServers`; skipping MCP reinjection.")
        return None, notes
    destination = temp_home / "additional-mcp-config.json"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(parsed, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    notes.append(f"Loaded MCP config from {source_path}")
    notes.extend(repairs)
    return destination, notes


def path_has_prefix(path: Path, prefix: Path) -> bool:
    return path == prefix or prefix in path.parents


def validate_workspace_root(repo_root: Path, workspace_root: Path) -> None:
    skills_root = (repo_root / ".github" / "skills").resolve()
    if path_has_prefix(workspace_root, skills_root):
        recommended_root = repo_root / "tests" / "skills"
        raise SystemExit(
            "Invalid --workspace-root: evaluation workspaces must live outside .github/skills.\n"
            f"Received: {workspace_root}\n"
            f"Recommended: {recommended_root}"
        )


def repo_copy_ignore(repo_root: Path, extra_ignored_prefixes: list[Path] | None = None):
    extra_ignored_prefixes = extra_ignored_prefixes or []

    def _ignore(src: str, names: list[str]) -> list[str]:
        ignored: list[str] = []
        src_path = Path(src)
        rel = src_path.relative_to(repo_root)
        for name in names:
            child_rel = rel / name if rel != Path(".") else Path(name)
            if name in IGNORED_TOP_LEVEL_NAMES:
                ignored.append(name)
                continue
            if child_rel.parts[:2] == ("tests", "skills"):
                ignored.append(name)
                continue
            if any(path_has_prefix(child_rel, prefix) for prefix in extra_ignored_prefixes):
                ignored.append(name)
                continue
            if Path(name).suffix in IGNORED_FILE_SUFFIXES:
                ignored.append(name)
                continue
        return ignored

    return _ignore


def copy_repo_to_sandbox(repo_root: Path, sandbox_repo_root: Path, extra_ignored_prefixes: list[Path] | None = None) -> None:
    shutil.copytree(repo_root, sandbox_repo_root, ignore=repo_copy_ignore(repo_root, extra_ignored_prefixes))


def materialize_old_skill_snapshot(snapshot_dir: Path, target_skill_dir: Path, skill_name: str) -> None:
    baseline_skill = snapshot_dir / "BASELINE_SKILL.md"
    if not baseline_skill.exists():
        raise SystemExit(
            f"old_skill requested, but snapshot file is missing: {baseline_skill}. "
            "Create tests/skills/<skill-name>-workspace/skill-snapshot/BASELINE_SKILL.md first."
        )
    target_skill_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(baseline_skill, target_skill_dir / "SKILL.md")
    direct_support_dir = snapshot_dir / skill_name
    if direct_support_dir.exists() and direct_support_dir.is_dir():
        for child in direct_support_dir.iterdir():
            destination = target_skill_dir / child.name
            if child.is_dir():
                shutil.copytree(child, destination)
            else:
                shutil.copy2(child, destination)
    for child in snapshot_dir.iterdir():
        if child.name in {"BASELINE_SKILL.md", skill_name}:
            continue
        destination = target_skill_dir / child.name
        if child.is_dir():
            shutil.copytree(child, destination)
        else:
            shutil.copy2(child, destination)


def materialize_skill_view(
    config: str,
    sandbox_repo_root: Path,
    repo_root: Path,
    skill_name: str,
    snapshot_dir: Path,
    without_skill_mode: str,
) -> tuple[Path, list[str]]:
    notes: list[str] = []
    skill_root = sandbox_repo_root / ".github" / "skills"
    target_skill_dir = skill_root / skill_name
    if config == "without_skill":
        if without_skill_mode == "no-repo-skills":
            if skill_root.exists():
                shutil.rmtree(skill_root)
            skill_root.mkdir(parents=True, exist_ok=True)
            notes.append("without_skill mode: removed all repository-local skills from the sandbox.")
        else:
            if target_skill_dir.exists():
                shutil.rmtree(target_skill_dir)
            notes.append("without_skill mode: removed only the target repository-local skill from the sandbox.")
        return target_skill_dir, notes
    if config == "old_skill":
        if target_skill_dir.exists():
            shutil.rmtree(target_skill_dir)
        materialize_old_skill_snapshot(snapshot_dir, target_skill_dir, skill_name)
        notes.append("Materialized BASELINE_SKILL.md as the active SKILL.md for old_skill.")
        return target_skill_dir, notes
    live_skill_dir = repo_root / ".github" / "skills" / skill_name
    if not live_skill_dir.exists():
        raise SystemExit(f"Live skill directory not found: {live_skill_dir}")
    if not (target_skill_dir / "SKILL.md").exists():
        raise SystemExit(f"Sandbox live skill is missing SKILL.md: {target_skill_dir / 'SKILL.md'}")
    notes.append("with_skill mode: kept the live repository-local skill visible in the sandbox.")
    return target_skill_dir, notes


def hash_file(path: Path) -> str:
    import hashlib

    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def collect_visible_skill_files(sandbox_repo_root: Path, target_skill_dir: Path) -> list[dict[str, str]]:
    if not target_skill_dir.exists():
        return []
    files: list[dict[str, str]] = []
    for path in sorted(p for p in target_skill_dir.rglob("*") if p.is_file()):
        files.append(
            {
                "path": str(path.relative_to(sandbox_repo_root)).replace("\\", "/"),
                "sha256": hash_file(path),
            }
        )
    return files


def validate_skill_visibility(
    config: str,
    target_skill_dir: Path,
    repo_root: Path,
    skill_name: str,
) -> list[str]:
    notes: list[str] = []
    active_skill_path = target_skill_dir / "SKILL.md"
    if config in {"with_skill", "old_skill"}:
        if not active_skill_path.exists():
            raise SystemExit(f"{config} sandbox is invalid: missing {active_skill_path}")
    if config == "without_skill" and target_skill_dir.exists():
        raise SystemExit(f"without_skill sandbox is invalid: target skill still exists at {target_skill_dir}")
    if config == "old_skill" and active_skill_path.exists():
        live_skill_path = repo_root / ".github" / "skills" / skill_name / "SKILL.md"
        if live_skill_path.exists():
            differs = hash_file(live_skill_path) != hash_file(active_skill_path)
            notes.append(f"old_skill differs_from_live={differs}")
    return notes


def parse_jsonl_events(raw_output: str) -> tuple[list[dict[str, Any]], list[str]]:
    events: list[dict[str, Any]] = []
    warnings: list[str] = []
    for line_number, line in enumerate(raw_output.splitlines(), start=1):
        stripped = line.strip()
        if not stripped:
            continue
        if not stripped.startswith("{"):
            warnings.append(f"Ignored non-JSONL output line {line_number}: {stripped[:120]}")
            continue
        try:
            payload = json.loads(stripped)
        except json.JSONDecodeError as exc:
            warnings.append(f"Ignored malformed JSONL line {line_number}: {exc.msg}")
            continue
        if isinstance(payload, dict):
            events.append(payload)
    return events, warnings


def extract_executor_result(events: list[dict[str, Any]], fallback_text: str) -> dict[str, Any]:
    assistant_messages = [event for event in events if event.get("type") == "assistant.message"]
    assistant_deltas = [event for event in events if event.get("type") == "assistant.message_delta"]
    result_events = [event for event in events if event.get("type") == "result"]
    response_parts: list[str] = []
    for event in assistant_messages:
        data = event.get("data") or {}
        content = data.get("content")
        if isinstance(content, str) and content:
            response_parts.append(content)
    response_text = "\n\n".join(response_parts).strip()
    if not response_text and assistant_deltas:
        response_text = "".join(
            str((event.get("data") or {}).get("deltaContent") or "") for event in assistant_deltas
        ).strip()
    if not response_text:
        response_text = fallback_text.strip()
    last_result = result_events[-1] if result_events else {}
    usage = last_result.get("usage") or {}
    output_tokens = 0
    tool_requests = 0
    for event in assistant_messages:
        data = event.get("data") or {}
        output_tokens += int(data.get("outputTokens") or 0)
        tool_requests += len(data.get("toolRequests") or [])
    session_duration_ms = int(usage.get("sessionDurationMs") or usage.get("totalApiDurationMs") or 0)
    return {
        "response_text": response_text,
        "output_tokens": output_tokens,
        "tool_requests": tool_requests,
        "session_duration_ms": session_duration_ms,
        "result_event": last_result,
    }


def run_copilot_prompt(
    *,
    prompt: str,
    cwd: Path,
    model: str,
    timeout_seconds: int,
    custom_instructions: bool,
    mcp_config_source: Path | None,
    use_mcp: bool,
) -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="skill-runner-home-") as temp_home_raw:
        temp_home = Path(temp_home_raw)
        prepare_isolated_home_fs(temp_home)
        env = build_isolated_env(temp_home)
        additional_mcp_config, mcp_notes = prepare_mcp_config(temp_home, mcp_config_source, enabled=use_mcp)
        command = [
            "gh",
            "copilot",
            "--",
            "-p",
            prompt,
            "--allow-all-tools",
            "--no-ask-user",
            "--output-format",
            "json",
            "--model",
            model,
        ]
        if not custom_instructions:
            command.append("--no-custom-instructions")
        if additional_mcp_config is not None:
            command.extend(["--additional-mcp-config", f"@{additional_mcp_config}"])
        try:
            completed = subprocess.run(
                command,
                cwd=str(cwd),
                env=env,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=timeout_seconds,
            )
        except subprocess.TimeoutExpired as exc:
            stdout = exc.stdout or ""
            stderr = exc.stderr or ""
            return {
                "command": command,
                "stdout": stdout,
                "stderr": stderr,
                "returncode": 124,
                "events": [],
                "warnings": [f"Copilot CLI call timed out after {timeout_seconds} seconds."],
                "response_text": stdout.strip() or stderr.strip(),
                "output_tokens": 0,
                "session_duration_ms": timeout_seconds * 1000,
                "tool_requests": 0,
                "mcp_notes": mcp_notes,
            }
        events, warnings = parse_jsonl_events(completed.stdout)
        extracted = extract_executor_result(events, completed.stdout or completed.stderr)
        return {
            "command": command,
            "stdout": completed.stdout,
            "stderr": completed.stderr,
            "returncode": completed.returncode,
            "events": events,
            "warnings": warnings,
            "response_text": extracted["response_text"],
            "output_tokens": extracted["output_tokens"],
            "session_duration_ms": extracted["session_duration_ms"],
            "tool_requests": extracted["tool_requests"],
            "mcp_notes": mcp_notes,
        }


def extract_json_object(text: str) -> dict[str, Any] | None:
    stripped = text.strip()
    if not stripped:
        return None
    fenced_match = re.search(r"```(?:json)?\s*(\{.*\})\s*```", stripped, flags=re.DOTALL)
    candidate = fenced_match.group(1) if fenced_match else stripped
    try:
        parsed = json.loads(candidate)
        return parsed if isinstance(parsed, dict) else None
    except json.JSONDecodeError:
        pass
    start = candidate.find("{")
    if start == -1:
        return None
    depth = 0
    in_string = False
    escape = False
    for idx in range(start, len(candidate)):
        char = candidate[idx]
        if in_string:
            if escape:
                escape = False
            elif char == "\\":
                escape = True
            elif char == '"':
                in_string = False
            continue
        if char == '"':
            in_string = True
            continue
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                snippet = candidate[start : idx + 1]
                try:
                    parsed = json.loads(snippet)
                    return parsed if isinstance(parsed, dict) else None
                except json.JSONDecodeError:
                    return None
    return None


def normalize_grading_payload(
    raw_payload: dict[str, Any] | None,
    expectations: list[str],
    *,
    response_text: str,
    executor_duration_seconds: float,
    grader_duration_seconds: float,
    executor_output_chars: int,
    total_tool_requests: int,
    executor_notes: list[str],
) -> dict[str, Any]:
    fallback_uncertainty = []
    if raw_payload is None:
        fallback_uncertainty.append("Grader response was not valid JSON; manual review recommended.")
    payload = raw_payload or {}
    raw_expectations = payload.get("expectations") or []
    normalized_expectations: list[dict[str, Any]] = []
    for index, text in enumerate(expectations):
        raw_entry = raw_expectations[index] if index < len(raw_expectations) and isinstance(raw_expectations[index], dict) else {}
        normalized_expectations.append(
            {
                "text": text,
                "passed": bool(raw_entry.get("passed")) if raw_entry else False,
                "evidence": str(raw_entry.get("evidence") or "Automated grader did not supply evidence."),
            }
        )
    passed = sum(1 for item in normalized_expectations if item["passed"])
    failed = sum(1 for item in normalized_expectations if not item["passed"])
    total = len(normalized_expectations)
    pass_rate = (passed / total) if total else 0.0
    user_notes_summary = payload.get("user_notes_summary") if isinstance(payload.get("user_notes_summary"), dict) else {}
    uncertainties = list(user_notes_summary.get("uncertainties") or [])
    uncertainties.extend(executor_notes)
    uncertainties.extend(fallback_uncertainty)
    normalized = {
        "expectations": normalized_expectations,
        "summary": {
            "passed": passed,
            "failed": failed,
            "total": total,
            "pass_rate": round(pass_rate, 4),
        },
        "execution_metrics": {
            "tool_calls": {},
            "total_tool_calls": total_tool_requests,
            "total_steps": 0,
            "errors_encountered": 0,
            "output_chars": executor_output_chars,
            "transcript_chars": executor_output_chars,
        },
        "timing": {
            "executor_duration_seconds": round(executor_duration_seconds, 3),
            "grader_duration_seconds": round(grader_duration_seconds, 3),
            "total_duration_seconds": round(executor_duration_seconds + grader_duration_seconds, 3),
        },
        "claims": payload.get("claims") if isinstance(payload.get("claims"), list) else [],
        "user_notes_summary": {
            "uncertainties": uncertainties,
            "needs_review": list(user_notes_summary.get("needs_review") or []),
            "workarounds": list(user_notes_summary.get("workarounds") or []),
        },
        "eval_feedback": payload.get("eval_feedback")
        if isinstance(payload.get("eval_feedback"), dict)
        else {"suggestions": [], "overall": "Automated grader completed for this iteration."},
    }
    return normalized


def build_grader_prompt(prompt: str, response_text: str, expectations: list[str]) -> str:
    expectations_json = json.dumps(expectations, ensure_ascii=False, indent=2)
    return textwrap.dedent(
        f"""
        Tu es un grader strict pour un benchmark de skill Copilot.

        Évalue uniquement la réponse candidate contre les assertions fournies.
        Retourne STRICTEMENT un objet JSON valide, sans markdown ni texte avant/après.

        Format attendu :
        {{
          "expectations": [
            {{"text": "<copie exacte de l'assertion>", "passed": true, "evidence": "citation courte ou absence explicite"}}
          ],
          "claims": [],
          "user_notes_summary": {{"uncertainties": [], "needs_review": [], "workarounds": []}},
          "eval_feedback": {{"suggestions": [], "overall": "appréciation brève"}}
        }}

        Règles :
        - Réutilise EXACTEMENT chaque texte d'assertion.
        - `passed` vaut true seulement si la réponse couvre clairement l'assertion.
        - `evidence` doit citer un extrait exact ou signaler l'absence de mention explicite.
        - Ne te base que sur le texte donné.

        Prompt utilisateur :
        {prompt}

        Réponse candidate :
        {response_text}

        Assertions JSON :
        {expectations_json}
        """
    ).strip()


def grade_response(
    *,
    prompt: str,
    response_text: str,
    expectations: list[str],
    model: str,
    timeout_seconds: int,
) -> tuple[dict[str, Any], dict[str, Any]]:
    if not expectations:
        placeholder = normalize_grading_payload(
            {"expectations": [], "user_notes_summary": {"uncertainties": [], "needs_review": [], "workarounds": []}},
            expectations,
            response_text=response_text,
            executor_duration_seconds=0.0,
            grader_duration_seconds=0.0,
            executor_output_chars=len(response_text),
            total_tool_requests=0,
            executor_notes=[],
        )
        return placeholder, {"raw_response": "", "output_tokens": 0, "session_duration_ms": 0}
    grader_prompt = build_grader_prompt(prompt, response_text, expectations)
    grader_result = run_copilot_prompt(
        prompt=grader_prompt,
        cwd=Path.cwd(),
        model=model,
        timeout_seconds=timeout_seconds,
        custom_instructions=False,
        mcp_config_source=None,
        use_mcp=False,
    )
    parsed_payload = extract_json_object(grader_result["response_text"])
    normalized = normalize_grading_payload(
        parsed_payload,
        expectations,
        response_text=response_text,
        executor_duration_seconds=0.0,
        grader_duration_seconds=grader_result["session_duration_ms"] / 1000,
        executor_output_chars=len(response_text),
        total_tool_requests=0,
        executor_notes=grader_result["warnings"] + grader_result["mcp_notes"],
    )
    return normalized, grader_result


def should_ignore_diff_path(
    relative_path: Path,
    skill_name: str,
    extra_ignored_prefixes: list[Path] | None = None,
) -> bool:
    extra_ignored_prefixes = extra_ignored_prefixes or []
    if relative_path.parts[:2] == ("tests", "skills"):
        return True
    if relative_path.parts[:3] == (".github", "skills", skill_name):
        return True
    if any(path_has_prefix(relative_path, prefix) for prefix in [*IGNORED_DIFF_PREFIXES, *extra_ignored_prefixes]):
        return True
    if any(part in IGNORED_TOP_LEVEL_NAMES for part in relative_path.parts):
        return True
    if relative_path.suffix in IGNORED_FILE_SUFFIXES:
        return True
    return False


def collect_repo_file_map(
    root: Path,
    *,
    skill_name: str,
    extra_ignored_prefixes: list[Path] | None = None,
) -> dict[Path, str]:
    file_map: dict[Path, str] = {}
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(root)
        if should_ignore_diff_path(rel, skill_name, extra_ignored_prefixes):
            continue
        file_map[rel] = hash_file(path)
    return file_map


def collect_workspace_diff(
    repo_root: Path,
    sandbox_repo_root: Path,
    skill_name: str,
    extra_ignored_prefixes: list[Path] | None = None,
) -> dict[str, Any]:
    original = collect_repo_file_map(
        repo_root,
        skill_name=skill_name,
        extra_ignored_prefixes=extra_ignored_prefixes,
    )
    sandbox = collect_repo_file_map(
        sandbox_repo_root,
        skill_name=skill_name,
        extra_ignored_prefixes=extra_ignored_prefixes,
    )
    added = sorted(str(path).replace("\\", "/") for path in sandbox.keys() - original.keys())
    deleted = sorted(str(path).replace("\\", "/") for path in original.keys() - sandbox.keys())
    modified = sorted(
        str(path).replace("\\", "/")
        for path in sandbox.keys() & original.keys()
        if sandbox[path] != original[path]
    )
    return {
        "added": added,
        "deleted": deleted,
        "modified": modified,
    }


def copy_changed_workspace_files(
    *,
    diff_payload: dict[str, Any],
    sandbox_repo_root: Path,
    outputs_dir: Path,
) -> None:
    changed_files = list(diff_payload.get("added") or []) + list(diff_payload.get("modified") or [])
    if not changed_files:
        return
    destination_root = outputs_dir / "workspace-files"
    for relative in changed_files:
        src = sandbox_repo_root / Path(relative)
        if not src.exists() or not src.is_file():
            continue
        destination = destination_root / Path(relative)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, destination)


def build_skill_manifest(
    *,
    skill_name: str,
    configuration: str,
    sandbox_repo_root: Path,
    visible_skill_files: list[dict[str, str]],
    manifest_notes: list[str],
    mcp_source: Path | None,
) -> dict[str, Any]:
    manifest: dict[str, Any] = {
        "skill_name": skill_name,
        "configuration": configuration,
        "sandbox_root": str(sandbox_repo_root),
        "visible_skill_files": visible_skill_files,
        "notes": manifest_notes,
    }
    if configuration == "without_skill":
        manifest["target_skill_visible"] = False
        manifest["absence_statement"] = "No target repository-local skill was visible in this sandbox."
    else:
        manifest["target_skill_visible"] = True
    if mcp_source is not None:
        manifest["mcp_config_source"] = str(mcp_source)
    return manifest


def run_single_eval(
    *,
    repo_root: Path,
    skill_name: str,
    snapshot_dir: Path,
    eval_def: dict[str, Any],
    eval_name: str,
    config: str,
    run_number: int,
    run_dir: Path,
    model: str,
    timeout_seconds: int,
    mcp_config_path: Path | None,
    use_mcp: bool,
    skip_grading: bool,
    without_skill_mode: str,
    copy_ignore_prefixes: list[Path],
) -> None:
    outputs_dir = run_dir / "outputs"
    outputs_dir.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=f"skill-sandbox-{skill_name}-{config}-") as sandbox_root_raw:
        sandbox_root = Path(sandbox_root_raw)
        sandbox_repo_root = sandbox_root / "repo"
        copy_repo_to_sandbox(repo_root, sandbox_repo_root, copy_ignore_prefixes)
        target_skill_dir, manifest_notes = materialize_skill_view(
            config,
            sandbox_repo_root,
            repo_root,
            skill_name,
            snapshot_dir,
            without_skill_mode,
        )
        manifest_notes.extend(validate_skill_visibility(config, target_skill_dir, repo_root, skill_name))
        visible_skill_files = collect_visible_skill_files(sandbox_repo_root, target_skill_dir)
        executor_result = run_copilot_prompt(
            prompt=str(eval_def["prompt"]),
            cwd=sandbox_repo_root,
            model=model,
            timeout_seconds=timeout_seconds,
            custom_instructions=True,
            mcp_config_source=mcp_config_path,
            use_mcp=use_mcp,
        )
        response_text = executor_result["response_text"].strip()
        (outputs_dir / "response.md").write_text(response_text + ("\n" if response_text else ""), encoding="utf-8")
        (run_dir / "executor.jsonl").write_text(executor_result["stdout"], encoding="utf-8")
        if executor_result["stderr"]:
            (run_dir / "executor.stderr.txt").write_text(executor_result["stderr"], encoding="utf-8")
        diff_payload = collect_workspace_diff(
            repo_root,
            sandbox_repo_root,
            skill_name,
            extra_ignored_prefixes=copy_ignore_prefixes,
        )
        write_json_file(run_dir / "workspace_diff.json", diff_payload)
        copy_changed_workspace_files(diff_payload=diff_payload, sandbox_repo_root=sandbox_repo_root, outputs_dir=outputs_dir)
        manifest_notes.extend(executor_result["warnings"])
        manifest_notes.extend(executor_result["mcp_notes"])
        write_json_file(
            run_dir / "skill_manifest.json",
            build_skill_manifest(
                skill_name=skill_name,
                configuration=config,
                sandbox_repo_root=sandbox_repo_root,
                visible_skill_files=visible_skill_files,
                manifest_notes=manifest_notes,
                mcp_source=mcp_config_path if use_mcp else None,
            ),
        )
        executor_duration_seconds = executor_result["session_duration_ms"] / 1000
        executor_output_tokens = int(executor_result["output_tokens"] or 0)
        expectations = list(eval_def.get("expectations") or [])
        if skip_grading:
            grading_payload = normalize_grading_payload(
                None,
                expectations,
                response_text=response_text,
                executor_duration_seconds=executor_duration_seconds,
                grader_duration_seconds=0.0,
                executor_output_chars=len(response_text),
                total_tool_requests=int(executor_result["tool_requests"] or 0),
                executor_notes=["Grader pass skipped via --skip-grading."] + manifest_notes,
            )
            grader_result = {"raw_response": "", "output_tokens": 0, "session_duration_ms": 0}
        else:
            grading_payload, grader_result = grade_response(
                prompt=str(eval_def["prompt"]),
                response_text=response_text,
                expectations=expectations,
                model=model,
                timeout_seconds=timeout_seconds,
            )
            grading_payload["execution_metrics"]["total_tool_calls"] = int(executor_result["tool_requests"] or 0)
            grading_payload["execution_metrics"]["output_chars"] = len(response_text)
            grading_payload["execution_metrics"]["transcript_chars"] = len(executor_result["stdout"])
            grading_payload["timing"] = {
                "executor_duration_seconds": round(executor_duration_seconds, 3),
                "grader_duration_seconds": round(grader_result["session_duration_ms"] / 1000, 3),
                "total_duration_seconds": round(executor_duration_seconds + (grader_result["session_duration_ms"] / 1000), 3),
            }
            uncertainties = list(grading_payload["user_notes_summary"].get("uncertainties") or [])
            uncertainties.extend(manifest_notes)
            grading_payload["user_notes_summary"]["uncertainties"] = uncertainties
            (run_dir / "grader.raw.txt").write_text(str(grader_result.get("response_text") or ""), encoding="utf-8")
            if grader_result.get("stdout"):
                (run_dir / "grader.stdout.txt").write_text(str(grader_result["stdout"]), encoding="utf-8")
            if grader_result.get("stderr"):
                (run_dir / "grader.stderr.txt").write_text(str(grader_result["stderr"]), encoding="utf-8")
        write_json_file(run_dir / "grading.json", grading_payload)
        write_json_file(
            run_dir / "timing.json",
            {
                "total_tokens": executor_output_tokens + int(grader_result.get("output_tokens") or 0),
                "duration_ms": int(executor_result["session_duration_ms"] or 0),
                "total_duration_seconds": round(executor_duration_seconds + (grader_result.get("session_duration_ms", 0) / 1000), 3),
                "executor_duration_seconds": round(executor_duration_seconds, 3),
                "grader_duration_seconds": round(grader_result.get("session_duration_ms", 0) / 1000, 3),
                "executor_output_tokens": executor_output_tokens,
                "grader_output_tokens": int(grader_result.get("output_tokens") or 0),
            },
        )


def mean_and_stddev(values: list[float]) -> dict[str, float]:
    if not values:
        return {"mean": 0.0, "stddev": 0.0, "min": 0.0, "max": 0.0}
    if len(values) == 1:
        value = float(values[0])
        return {"mean": round(value, 4), "stddev": 0.0, "min": round(value, 4), "max": round(value, 4)}
    return {
        "mean": round(statistics.mean(values), 4),
        "stddev": round(statistics.pstdev(values), 4),
        "min": round(min(values), 4),
        "max": round(max(values), 4),
    }


def aggregate_iteration(
    *,
    repo_root: Path,
    skill_name: str,
    iteration_dir: Path,
    model: str,
    baseline_config: str,
    mcp_enabled: bool,
) -> dict[str, Any]:
    runs: list[dict[str, Any]] = []
    per_config_pass_rates: dict[str, list[float]] = {}
    per_config_times: dict[str, list[float]] = {}
    per_config_tokens: dict[str, list[float]] = {}
    for eval_dir in sorted(path for path in iteration_dir.iterdir() if path.is_dir()):
        metadata_path = eval_dir / "eval_metadata.json"
        if not metadata_path.exists():
            continue
        metadata = load_json_file(metadata_path)
        for config_dir in sorted(path for path in eval_dir.iterdir() if path.is_dir() and path.name in CONFIG_ORDER):
            for run_dir in sorted(path for path in config_dir.iterdir() if path.is_dir() and path.name.startswith("run-")):
                grading = load_json_file(run_dir / "grading.json")
                timing = load_json_file(run_dir / "timing.json")
                manifest = load_json_file(run_dir / "skill_manifest.json")
                pass_rate = float((grading.get("summary") or {}).get("pass_rate") or 0.0)
                executor_time = float(timing.get("executor_duration_seconds") or 0.0)
                executor_tokens = float(timing.get("executor_output_tokens") or timing.get("total_tokens") or 0.0)
                configuration = config_dir.name
                per_config_pass_rates.setdefault(configuration, []).append(pass_rate)
                per_config_times.setdefault(configuration, []).append(executor_time)
                per_config_tokens.setdefault(configuration, []).append(executor_tokens)
                run_number_match = re.match(r"run-(\d+)$", run_dir.name)
                run_number = int(run_number_match.group(1)) if run_number_match else 1
                notes = list(((grading.get("user_notes_summary") or {}).get("uncertainties") or []))
                if configuration == "without_skill":
                    notes.append(f"without_skill mode: {manifest.get('notes', [])[-1] if manifest.get('notes') else 'target skill hidden.'}")
                runs.append(
                    {
                        "eval_id": metadata.get("eval_id"),
                        "configuration": configuration,
                        "run_number": run_number,
                        "result": {
                            "pass_rate": pass_rate,
                            "passed": int((grading.get("summary") or {}).get("passed") or 0),
                            "failed": int((grading.get("summary") or {}).get("failed") or 0),
                            "total": int((grading.get("summary") or {}).get("total") or 0),
                            "time_seconds": executor_time,
                            "tokens": executor_tokens,
                            "tool_calls": int((grading.get("execution_metrics") or {}).get("total_tool_calls") or 0),
                            "errors": int((grading.get("execution_metrics") or {}).get("errors_encountered") or 0),
                        },
                        "expectations": grading.get("expectations") or [],
                        "notes": notes,
                        "eval_name": metadata.get("eval_name"),
                    }
                )
    ordered_present_configs = [config for config in CONFIG_ORDER if config in per_config_pass_rates]
    run_summary: dict[str, Any] = {}
    for config in ordered_present_configs:
        run_summary[config] = {
            "pass_rate": mean_and_stddev(per_config_pass_rates.get(config, [])),
            "time_seconds": mean_and_stddev(per_config_times.get(config, [])),
            "tokens": mean_and_stddev(per_config_tokens.get(config, [])),
        }
    primary_mean = run_summary.get(PRIMARY_CONFIG, {}).get("pass_rate", {}).get("mean", 0.0)
    baseline_mean = run_summary.get(baseline_config, {}).get("pass_rate", {}).get("mean", 0.0)
    primary_time = run_summary.get(PRIMARY_CONFIG, {}).get("time_seconds", {}).get("mean", 0.0)
    baseline_time = run_summary.get(baseline_config, {}).get("time_seconds", {}).get("mean", 0.0)
    primary_tokens = run_summary.get(PRIMARY_CONFIG, {}).get("tokens", {}).get("mean", 0.0)
    baseline_tokens = run_summary.get(baseline_config, {}).get("tokens", {}).get("mean", 0.0)
    run_summary["delta"] = {
        "pass_rate": format_delta(primary_mean - baseline_mean),
        "time_seconds": format_delta(primary_time - baseline_time),
        "tokens": format_delta(primary_tokens - baseline_tokens),
    }
    notes = [
        f"Primary configuration: {PRIMARY_CONFIG}; baseline: {baseline_config}.",
        "Time metrics come from Copilot CLI sessionDurationMs.",
        "Token metrics use assistant output tokens from executor runs only; full prompt-side token counts are not exposed by Copilot CLI JSONL.",
        "Repository-local skill leakage is reduced by isolated HOME/USERPROFILE/COPILOT_HOME per run.",
    ]
    if mcp_enabled:
        notes.append("Isolated runs re-inject MCP servers from ~/.vscode/mcp.json when that file is available and can be sanitized.")
    benchmark = {
        "metadata": {
            "skill_name": skill_name,
            "skill_path": str((repo_root / ".github" / "skills" / skill_name).resolve()),
            "executor_model": model,
            "analyzer_model": model,
            "timestamp": utc_now_iso(),
            "evals_run": sorted({run["eval_id"] for run in runs if isinstance(run.get("eval_id"), int)}),
            "runs_per_configuration": max((run.get("run_number") or 0) for run in runs) if runs else 0,
        },
        "runs": runs,
        "run_summary": run_summary,
        "notes": notes,
    }
    return benchmark


def write_benchmark_markdown(iteration_dir: Path, benchmark: dict[str, Any], baseline_config: str) -> None:
    run_summary = benchmark.get("run_summary") or {}
    configurations = [config for config in CONFIG_ORDER if config in run_summary]
    lines = [
        f"# Benchmark — {benchmark['metadata']['skill_name']}",
        "",
        f"- Timestamp: {benchmark['metadata']['timestamp']}",
        f"- Primary configuration: `{PRIMARY_CONFIG}`",
        f"- Baseline: `{baseline_config}`",
        "",
        "| Configuration | Pass rate | Time (s) | Tokens |",
        "|---|---:|---:|---:|",
    ]
    for config in configurations:
        summary = run_summary[config]
        lines.append(
            "| {config} | {pass_rate} | {time_seconds} | {tokens} |".format(
                config=config,
                pass_rate=format_stat(summary["pass_rate"]["mean"], summary["pass_rate"]["stddev"], is_percent=True),
                time_seconds=format_stat(summary["time_seconds"]["mean"], summary["time_seconds"]["stddev"]),
                tokens=format_stat(summary["tokens"]["mean"], summary["tokens"]["stddev"]),
            )
        )
    delta = run_summary.get("delta") or {}
    lines.extend(
        [
            "",
            "## Delta",
            "",
            f"- Pass rate: `{delta.get('pass_rate', '+0.00')}`",
            f"- Time seconds: `{delta.get('time_seconds', '+0.00')}`",
            f"- Tokens: `{delta.get('tokens', '+0.00')}`",
            "",
            "## Notes",
            "",
        ]
    )
    for note in benchmark.get("notes") or []:
        lines.append(f"- {note}")
    (iteration_dir / "benchmark.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def html_escape(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#39;")
    )


def write_review_html(iteration_dir: Path, benchmark: dict[str, Any]) -> None:
    configurations = [config for config in CONFIG_ORDER if config in (benchmark.get("run_summary") or {})]
    summary_rows = []
    for config in configurations:
        summary = benchmark["run_summary"][config]
        summary_rows.append(
            "<tr><td><code>{config}</code></td><td>{pass_rate}</td><td>{time_seconds}</td><td>{tokens}</td></tr>".format(
                config=html_escape(config),
                pass_rate=html_escape(format_stat(summary["pass_rate"]["mean"], summary["pass_rate"]["stddev"], is_percent=True)),
                time_seconds=html_escape(format_stat(summary["time_seconds"]["mean"], summary["time_seconds"]["stddev"])),
                tokens=html_escape(format_stat(summary["tokens"]["mean"], summary["tokens"]["stddev"])),
            )
        )
    run_items = []
    for run in benchmark.get("runs") or []:
        eval_name = str(run.get("eval_name") or f"eval-{run.get('eval_id')}")
        configuration = str(run.get("configuration") or "")
        run_number = int(run.get("run_number") or 1)
        rel_base = Path(eval_name) / configuration / f"run-{run_number}"
        output_link = rel_base / "outputs" / "response.md"
        grading_link = rel_base / "grading.json"
        timing_link = rel_base / "timing.json"
        manifest_link = rel_base / "skill_manifest.json"
        pass_rate = float((run.get("result") or {}).get("pass_rate") or 0.0)
        run_items.append(
            "<li><strong>{eval_name}</strong> — <code>{configuration}</code> — pass rate {pass_rate} "
            "[<a href=\"{output_link}\">response</a>] "
            "[<a href=\"{grading_link}\">grading</a>] "
            "[<a href=\"{timing_link}\">timing</a>] "
            "[<a href=\"{manifest_link}\">manifest</a>]"
            "</li>".format(
                eval_name=html_escape(eval_name),
                configuration=html_escape(configuration),
                pass_rate=html_escape(format_percent(pass_rate)),
                output_link=html_escape(str(output_link).replace("\\", "/")),
                grading_link=html_escape(str(grading_link).replace("\\", "/")),
                timing_link=html_escape(str(timing_link).replace("\\", "/")),
                manifest_link=html_escape(str(manifest_link).replace("\\", "/")),
            )
        )
    html = f"""<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
  <title>Skill review — {html_escape(str(benchmark['metadata']['skill_name']))}</title>
  <style>
    body {{ font-family: Segoe UI, Arial, sans-serif; margin: 2rem; line-height: 1.5; }}
    code {{ background: #f3f4f6; padding: 0.1rem 0.25rem; border-radius: 4px; }}
    table {{ border-collapse: collapse; width: 100%; max-width: 960px; }}
    th, td {{ border: 1px solid #d1d5db; padding: 0.5rem; text-align: left; }}
    th {{ background: #f9fafb; }}
    ul {{ max-width: 960px; }}
  </style>
</head>
<body>
  <h1>Skill review — {html_escape(str(benchmark['metadata']['skill_name']))}</h1>
  <p>See also <a href=\"benchmark.md\">benchmark.md</a> and <a href=\"benchmark.json\">benchmark.json</a>.</p>

  <h2>Summary</h2>
  <table>
    <thead>
      <tr><th>Configuration</th><th>Pass rate</th><th>Time (s)</th><th>Tokens</th></tr>
    </thead>
    <tbody>
      {''.join(summary_rows)}
    </tbody>
  </table>

  <h2>Runs</h2>
  <ul>
    {''.join(run_items)}
  </ul>

  <h2>Notes</h2>
  <ul>
    {''.join(f'<li>{html_escape(str(note))}</li>' for note in (benchmark.get('notes') or []))}
  </ul>
</body>
</html>
"""
    (iteration_dir / "review.html").write_text(html, encoding="utf-8")


def discover_skill_names(repo_root: Path) -> list[str]:
    skills_root = repo_root / ".github" / "skills"
    return sorted(path.parent.parent.name for path in skills_root.glob("*/evals/evals.json"))


def choose_baseline_config(run_summary: dict[str, Any]) -> str | None:
    if "old_skill" in run_summary:
        return "old_skill"
    if "without_skill" in run_summary:
        return "without_skill"
    return None


def summary_metric(run_summary: dict[str, Any], config: str | None, metric: str) -> float | None:
    if config is None:
        return None
    config_summary = run_summary.get(config) or {}
    metric_summary = config_summary.get(metric) or {}
    mean = metric_summary.get("mean")
    return float(mean) if mean is not None else None


def format_optional_percent(value: float | None) -> str:
    return format_percent(value) if value is not None else "-"


def format_optional_delta(value: str | None) -> str:
    return value or "-"


def build_iteration_summary(iteration_dir: Path, benchmark: dict[str, Any]) -> dict[str, Any]:
    run_summary = benchmark.get("run_summary") or {}
    primary_config = PRIMARY_CONFIG if PRIMARY_CONFIG in run_summary else None
    baseline_config = choose_baseline_config(run_summary)
    return {
        "iteration": iteration_key(iteration_dir),
        "timestamp": str((benchmark.get("metadata") or {}).get("timestamp") or ""),
        "evals_run": list((benchmark.get("metadata") or {}).get("evals_run") or []),
        "runs_per_configuration": int((benchmark.get("metadata") or {}).get("runs_per_configuration") or 0),
        "primary_config": primary_config,
        "baseline_config": baseline_config,
        "primary_pass_rate": summary_metric(run_summary, primary_config, "pass_rate"),
        "baseline_pass_rate": summary_metric(run_summary, baseline_config, "pass_rate"),
        "primary_time_seconds": summary_metric(run_summary, primary_config, "time_seconds"),
        "baseline_time_seconds": summary_metric(run_summary, baseline_config, "time_seconds"),
        "primary_tokens": summary_metric(run_summary, primary_config, "tokens"),
        "baseline_tokens": summary_metric(run_summary, baseline_config, "tokens"),
        "delta": dict(run_summary.get("delta") or {}),
        "run_summary": run_summary,
        "notes": list(benchmark.get("notes") or []),
        "benchmark_json_path": str((iteration_dir / "benchmark.json").name).replace("\\", "/"),
        "benchmark_markdown_path": str((iteration_dir / "benchmark.md").name).replace("\\", "/"),
        "review_path": str((iteration_dir / "review.html").name).replace("\\", "/"),
    }


def build_workspace_history(workspace_dir: Path, skill_name: str) -> dict[str, Any]:
    iterations: list[dict[str, Any]] = []
    for iteration_dir in sorted((path for path in workspace_dir.glob("iteration-*") if path.is_dir()), key=iteration_key):
        benchmark_path = iteration_dir / "benchmark.json"
        if not benchmark_path.exists():
            continue
        benchmark = load_json_file(benchmark_path)
        iteration_summary = build_iteration_summary(iteration_dir, benchmark)
        iteration_summary["benchmark_json_path"] = str(benchmark_path.relative_to(workspace_dir)).replace("\\", "/")
        iteration_summary["benchmark_markdown_path"] = str((iteration_dir / "benchmark.md").relative_to(workspace_dir)).replace("\\", "/")
        iteration_summary["review_path"] = str((iteration_dir / "review.html").relative_to(workspace_dir)).replace("\\", "/")
        iterations.append(iteration_summary)
    latest = iterations[-1] if iterations else None
    return {
        "skill_name": skill_name,
        "workspace_dirname": workspace_dir.name,
        "generated_at": utc_now_iso(),
        "workspace_path": str(workspace_dir),
        "iteration_count": len(iterations),
        "latest_iteration": latest.get("iteration") if latest else None,
        "latest_timestamp": latest.get("timestamp") if latest else None,
        "latest_primary_pass_rate": latest.get("primary_pass_rate") if latest else None,
        "latest_baseline_pass_rate": latest.get("baseline_pass_rate") if latest else None,
        "latest_delta": dict(latest.get("delta") or {}) if latest else {},
        "iterations": iterations,
    }


def write_workspace_history_markdown(workspace_dir: Path, history_payload: dict[str, Any]) -> None:
    lines = [
        f"# Workspace history — {history_payload['skill_name']}",
        "",
        f"- Generated: {history_payload['generated_at']}",
        f"- Workspace: `{history_payload['workspace_dirname']}`",
        f"- Iterations with benchmark data: {history_payload['iteration_count']}",
        "",
    ]
    iterations = list(history_payload.get("iterations") or [])
    if not iterations:
        lines.extend([
            "No `benchmark.json` found yet in this workspace.",
            "",
        ])
    else:
        lines.extend(
            [
                "## Iterations",
                "",
                "| Iteration | Timestamp | Primary pass | Baseline pass | Delta | Benchmark | Review |",
                "|---:|---|---:|---:|---:|---|---|",
            ]
        )
        for item in reversed(iterations):
            lines.append(
                "| {iteration} | {timestamp} | {primary_pass} | {baseline_pass} | {delta} | [benchmark]({benchmark}) | [review]({review}) |".format(
                    iteration=item["iteration"],
                    timestamp=item["timestamp"] or "-",
                    primary_pass=format_optional_percent(item.get("primary_pass_rate")),
                    baseline_pass=format_optional_percent(item.get("baseline_pass_rate")),
                    delta=format_optional_delta((item.get("delta") or {}).get("pass_rate")),
                    benchmark=item["benchmark_markdown_path"],
                    review=item["review_path"],
                )
            )
        latest = iterations[-1]
        lines.extend(
            [
                "",
                "## Latest snapshot",
                "",
                f"- Iteration: `{latest['iteration']}`",
                f"- Timestamp: {latest['timestamp'] or '-'}",
                f"- Primary pass rate: {format_optional_percent(latest.get('primary_pass_rate'))}",
                f"- Baseline pass rate: {format_optional_percent(latest.get('baseline_pass_rate'))}",
                f"- Delta: {format_optional_delta((latest.get('delta') or {}).get('pass_rate'))}",
                f"- Benchmark JSON: `{latest['benchmark_json_path']}`",
                f"- Review HTML: `{latest['review_path']}`",
                "",
            ]
        )
    (workspace_dir / "workspace-history.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_workspace_history_html(workspace_dir: Path, history_payload: dict[str, Any]) -> None:
    iterations = list(history_payload.get("iterations") or [])
    if iterations:
        rows = "".join(
            "<tr><td>{iteration}</td><td>{timestamp}</td><td>{primary}</td><td>{baseline}</td><td>{delta}</td>"
            "<td><a href=\"{benchmark}\">benchmark</a></td><td><a href=\"{review}\">review</a></td></tr>".format(
                iteration=html_escape(str(item["iteration"])),
                timestamp=html_escape(item["timestamp"] or "-"),
                primary=html_escape(format_optional_percent(item.get("primary_pass_rate"))),
                baseline=html_escape(format_optional_percent(item.get("baseline_pass_rate"))),
                delta=html_escape(format_optional_delta((item.get("delta") or {}).get("pass_rate"))),
                benchmark=html_escape(item["benchmark_markdown_path"]),
                review=html_escape(item["review_path"]),
            )
            for item in reversed(iterations)
        )
        body = (
            "<table><thead><tr><th>Iteration</th><th>Timestamp</th><th>Primary pass</th><th>Baseline pass</th>"
            "<th>Delta</th><th>Benchmark</th><th>Review</th></tr></thead><tbody>{rows}</tbody></table>"
        ).format(rows=rows)
    else:
        body = "<p>No <code>benchmark.json</code> found yet in this workspace.</p>"
    html = f"""<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
  <title>Workspace history — {html_escape(history_payload['skill_name'])}</title>
  <style>
    body {{ font-family: Segoe UI, Arial, sans-serif; margin: 2rem; line-height: 1.5; }}
    code {{ background: #f3f4f6; padding: 0.1rem 0.25rem; border-radius: 4px; }}
    table {{ border-collapse: collapse; width: 100%; max-width: 1080px; }}
    th, td {{ border: 1px solid #d1d5db; padding: 0.5rem; text-align: left; }}
    th {{ background: #f9fafb; }}
  </style>
</head>
<body>
  <h1>Workspace history — {html_escape(history_payload['skill_name'])}</h1>
  <p>Generated {html_escape(history_payload['generated_at'])}. Workspace: <code>{html_escape(history_payload['workspace_dirname'])}</code>.</p>
  {body}
</body>
</html>
"""
    (workspace_dir / "workspace-history.html").write_text(html, encoding="utf-8")


def build_global_overview(repo_root: Path, workspace_root: Path, workspace_histories: list[dict[str, Any]]) -> dict[str, Any]:
    histories_by_skill = {payload["skill_name"]: payload for payload in workspace_histories}
    all_iterations: list[dict[str, Any]] = []
    latest_iterations: list[dict[str, Any]] = []
    for skill_name in discover_skill_names(repo_root):
        history = histories_by_skill.get(skill_name)
        if history is None:
            latest_iterations.append(
                {
                    "skill_name": skill_name,
                    "workspace_dirname": f"{skill_name}-workspace",
                    "history_markdown_path": None,
                    "history_html_path": None,
                    "iteration": None,
                    "timestamp": None,
                    "primary_pass_rate": None,
                    "baseline_pass_rate": None,
                    "delta": {},
                    "review_path": None,
                    "benchmark_path": None,
                    "iteration_count": 0,
                }
            )
            continue
        history_markdown_path = f"{history['workspace_dirname']}/workspace-history.md"
        history_html_path = f"{history['workspace_dirname']}/workspace-history.html"
        iterations = list(history.get("iterations") or [])
        for item in iterations:
            all_iterations.append(
                {
                    "skill_name": skill_name,
                    "workspace_dirname": history["workspace_dirname"],
                    "history_markdown_path": history_markdown_path,
                    "history_html_path": history_html_path,
                    "iteration": item.get("iteration"),
                    "timestamp": item.get("timestamp"),
                    "primary_pass_rate": item.get("primary_pass_rate"),
                    "baseline_pass_rate": item.get("baseline_pass_rate"),
                    "delta": dict(item.get("delta") or {}),
                    "review_path": f"{history['workspace_dirname']}/{item['review_path']}",
                    "benchmark_path": f"{history['workspace_dirname']}/{item['benchmark_markdown_path']}",
                }
            )
        latest = iterations[-1] if iterations else None
        latest_iterations.append(
            {
                "skill_name": skill_name,
                "workspace_dirname": history["workspace_dirname"],
                "history_markdown_path": history_markdown_path,
                "history_html_path": history_html_path,
                "iteration": latest.get("iteration") if latest else None,
                "timestamp": latest.get("timestamp") if latest else None,
                "primary_pass_rate": latest.get("primary_pass_rate") if latest else None,
                "baseline_pass_rate": latest.get("baseline_pass_rate") if latest else None,
                "delta": dict(latest.get("delta") or {}) if latest else {},
                "review_path": f"{history['workspace_dirname']}/{latest['review_path']}" if latest else None,
                "benchmark_path": f"{history['workspace_dirname']}/{latest['benchmark_markdown_path']}" if latest else None,
                "iteration_count": len(iterations),
            }
        )
    return {
        "generated_at": utc_now_iso(),
        "workspace_root": str(workspace_root),
        "skills_total": len(discover_skill_names(repo_root)),
        "skills_with_history": sum(1 for payload in workspace_histories if payload.get("iterations")),
        "iterations_total": len(all_iterations),
        "latest_iterations": latest_iterations,
        "all_iterations": sorted(
            all_iterations,
            key=lambda item: (str(item["skill_name"]), int(item["iteration"] or 0)),
        ),
    }


def write_global_overview_markdown(workspace_root: Path, overview: dict[str, Any]) -> None:
    lines = [
        "# Skill evaluation overview",
        "",
        f"- Generated: {overview['generated_at']}",
        f"- Workspace root: `{overview['workspace_root']}`",
        f"- Skills discovered: {overview['skills_total']}",
        f"- Skills with benchmark history: {overview['skills_with_history']}",
        f"- Iterations aggregated: {overview['iterations_total']}",
        "",
        "## Latest iteration per skill",
        "",
        "| Skill | Benchmarks | Latest | Timestamp | Primary pass | Baseline pass | Delta | History | Review |",
        "|---|---:|---:|---|---:|---:|---:|---|---|",
    ]
    for item in overview.get("latest_iterations") or []:
        history_link = f"[history]({item['history_markdown_path']})" if item.get("history_markdown_path") else "-"
        review_link = f"[review]({item['review_path']})" if item.get("review_path") else "-"
        lines.append(
            "| {skill} | {count} | {iteration} | {timestamp} | {primary} | {baseline} | {delta} | {history} | {review} |".format(
                skill=item["skill_name"],
                count=item.get("iteration_count", 0),
                iteration=item.get("iteration") or "-",
                timestamp=item.get("timestamp") or "-",
                primary=format_optional_percent(item.get("primary_pass_rate")),
                baseline=format_optional_percent(item.get("baseline_pass_rate")),
                delta=format_optional_delta((item.get("delta") or {}).get("pass_rate")),
                history=history_link,
                review=review_link,
            )
        )
    lines.extend(
        [
            "",
            "## All iterations",
            "",
            "| Skill | Iteration | Timestamp | Primary pass | Baseline pass | Delta | Benchmark |",
            "|---|---:|---|---:|---:|---:|---|",
        ]
    )
    for item in overview.get("all_iterations") or []:
        lines.append(
            "| {skill} | {iteration} | {timestamp} | {primary} | {baseline} | {delta} | [benchmark]({benchmark}) |".format(
                skill=item["skill_name"],
                iteration=item.get("iteration") or "-",
                timestamp=item.get("timestamp") or "-",
                primary=format_optional_percent(item.get("primary_pass_rate")),
                baseline=format_optional_percent(item.get("baseline_pass_rate")),
                delta=format_optional_delta((item.get("delta") or {}).get("pass_rate")),
                benchmark=item.get("benchmark_path") or "#",
            )
        )
    (workspace_root / "skills-overview.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_global_overview_html(workspace_root: Path, overview: dict[str, Any]) -> None:
    latest_rows = "".join(
        "<tr><td>{skill}</td><td>{count}</td><td>{iteration}</td><td>{timestamp}</td><td>{primary}</td><td>{baseline}</td><td>{delta}</td>"
        "<td>{history}</td><td>{review}</td></tr>".format(
            skill=html_escape(item["skill_name"]),
            count=html_escape(str(item.get("iteration_count", 0))),
            iteration=html_escape(str(item.get("iteration") or "-")),
            timestamp=html_escape(item.get("timestamp") or "-"),
            primary=html_escape(format_optional_percent(item.get("primary_pass_rate"))),
            baseline=html_escape(format_optional_percent(item.get("baseline_pass_rate"))),
            delta=html_escape(format_optional_delta((item.get("delta") or {}).get("pass_rate"))),
            history=(
                f'<a href="{html_escape(item["history_html_path"])}">history</a>' if item.get("history_html_path") else "-"
            ),
            review=(f'<a href="{html_escape(item["review_path"])}">review</a>' if item.get("review_path") else "-"),
        )
        for item in overview.get("latest_iterations") or []
    )
    all_rows = "".join(
        "<tr><td>{skill}</td><td>{iteration}</td><td>{timestamp}</td><td>{primary}</td><td>{baseline}</td><td>{delta}</td>"
        "<td><a href=\"{benchmark}\">benchmark</a></td></tr>".format(
            skill=html_escape(item["skill_name"]),
            iteration=html_escape(str(item.get("iteration") or "-")),
            timestamp=html_escape(item.get("timestamp") or "-"),
            primary=html_escape(format_optional_percent(item.get("primary_pass_rate"))),
            baseline=html_escape(format_optional_percent(item.get("baseline_pass_rate"))),
            delta=html_escape(format_optional_delta((item.get("delta") or {}).get("pass_rate"))),
            benchmark=html_escape(item.get("benchmark_path") or "#"),
        )
        for item in overview.get("all_iterations") or []
    )
    html = f"""<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
  <title>Skill evaluation overview</title>
  <style>
    body {{ font-family: Segoe UI, Arial, sans-serif; margin: 2rem; line-height: 1.5; }}
    code {{ background: #f3f4f6; padding: 0.1rem 0.25rem; border-radius: 4px; }}
    table {{ border-collapse: collapse; width: 100%; max-width: 1200px; margin-bottom: 2rem; }}
    th, td {{ border: 1px solid #d1d5db; padding: 0.5rem; text-align: left; }}
    th {{ background: #f9fafb; }}
  </style>
</head>
<body>
  <h1>Skill evaluation overview</h1>
  <p>Generated {html_escape(overview['generated_at'])}. Aggregated from <code>{html_escape(overview['workspace_root'])}</code>.</p>
  <p>Skills discovered: {html_escape(str(overview['skills_total']))}. Skills with benchmark history: {html_escape(str(overview['skills_with_history']))}. Iterations aggregated: {html_escape(str(overview['iterations_total']))}.</p>

  <h2>Latest iteration per skill</h2>
  <table>
    <thead>
            <tr><th>Skill</th><th>Benchmarks</th><th>Latest</th><th>Timestamp</th><th>Primary pass</th><th>Baseline pass</th><th>Delta</th><th>History</th><th>Review</th></tr>
    </thead>
    <tbody>{latest_rows}</tbody>
  </table>

  <h2>All iterations</h2>
  <table>
    <thead>
      <tr><th>Skill</th><th>Iteration</th><th>Timestamp</th><th>Primary pass</th><th>Baseline pass</th><th>Delta</th><th>Benchmark</th></tr>
    </thead>
    <tbody>{all_rows}</tbody>
  </table>
</body>
</html>
"""
    (workspace_root / "skills-overview.html").write_text(html, encoding="utf-8")


def refresh_workspace_and_global_reports(repo_root: Path, workspace_root: Path) -> dict[str, Any]:
    workspace_root.mkdir(parents=True, exist_ok=True)
    workspace_histories: list[dict[str, Any]] = []
    for skill_name in discover_skill_names(repo_root):
        workspace_dir = workspace_root / f"{skill_name}-workspace"
        if not workspace_dir.exists():
            continue
        history_payload = build_workspace_history(workspace_dir, skill_name)
        write_json_file(workspace_dir / "workspace-history.json", history_payload)
        write_workspace_history_markdown(workspace_dir, history_payload)
        write_workspace_history_html(workspace_dir, history_payload)
        workspace_histories.append(history_payload)
    overview = build_global_overview(repo_root, workspace_root, workspace_histories)
    write_json_file(workspace_root / "skills-overview.json", overview)
    write_global_overview_markdown(workspace_root, overview)
    write_global_overview_html(workspace_root, overview)
    return {
        "workspace_histories": workspace_histories,
        "overview": overview,
        "overview_json_path": workspace_root / "skills-overview.json",
        "overview_markdown_path": workspace_root / "skills-overview.md",
        "overview_html_path": workspace_root / "skills-overview.html",
    }


def run_skill(
    *,
    repo_root: Path,
    workspace_root: Path,
    skill_name: str,
    eval_ids: list[int] | None,
    configs: list[str] | None,
    runs_per_configuration: int,
    model: str,
    timeout_seconds: int,
    force_iteration: int | None,
    mcp_config: Path,
    no_mcp: bool,
    skip_grading: bool,
    without_skill_mode: str,
) -> Path:
    skill_dir = repo_root / ".github" / "skills" / skill_name
    if not skill_dir.exists():
        raise SystemExit(f"Skill directory not found: {skill_dir}")
    evals_path = skill_dir / "evals" / "evals.json"
    if not evals_path.exists():
        raise SystemExit(f"evals.json not found: {evals_path}")
    workspace_dir = workspace_root / f"{skill_name}-workspace"
    snapshot_dir = workspace_dir / "skill-snapshot"
    resolved_configs = configs or default_configs(snapshot_dir)
    if "old_skill" in resolved_configs and not (snapshot_dir / "BASELINE_SKILL.md").exists():
        raise SystemExit(
            f"Configuration old_skill requested, but snapshot is missing: {snapshot_dir / 'BASELINE_SKILL.md'}"
        )
    evals_payload = load_json_file(evals_path)
    evals = list(evals_payload.get("evals") or [])
    if eval_ids:
        allowed = set(eval_ids)
        evals = [eval_def for eval_def in evals if int(eval_def.get("id")) in allowed]
    if not evals:
        raise SystemExit("No evals selected to run.")
    workspace_dir.mkdir(parents=True, exist_ok=True)
    iteration_number = determine_iteration(workspace_dir, force_iteration)
    iteration_dir = workspace_dir / f"iteration-{iteration_number}"
    previous_names = load_previous_eval_names(workspace_dir)
    copy_ignore_prefixes: list[Path] = []
    try:
        if workspace_root.is_relative_to(repo_root):
            copy_ignore_prefixes.append(workspace_root.relative_to(repo_root))
    except ValueError:
        pass

    log(f"[1/4] Running skill evals for `{skill_name}` into `{iteration_dir}`")
    log(f"      Configurations: {', '.join(resolved_configs)}")
    log(f"      Eval IDs: {', '.join(str(eval_def['id']) for eval_def in evals)}")

    for eval_def in evals:
        eval_name = derive_eval_name(eval_def, previous_names)
        eval_dir = iteration_dir / eval_name
        eval_dir.mkdir(parents=True, exist_ok=True)
        write_json_file(
            eval_dir / "eval_metadata.json",
            {
                "eval_id": int(eval_def["id"]),
                "eval_name": eval_name,
                "prompt": str(eval_def["prompt"]),
                "assertions": list(eval_def.get("expectations") or []),
            },
        )
        for config in resolved_configs:
            for run_number in range(1, runs_per_configuration + 1):
                run_dir = eval_dir / config / f"run-{run_number}"
                log(f"[2/4] {eval_name} — {config} — run-{run_number}")
                run_single_eval(
                    repo_root=repo_root,
                    skill_name=skill_name,
                    snapshot_dir=snapshot_dir,
                    eval_def=eval_def,
                    eval_name=eval_name,
                    config=config,
                    run_number=run_number,
                    run_dir=run_dir,
                    model=model,
                    timeout_seconds=timeout_seconds,
                    mcp_config_path=mcp_config,
                    use_mcp=not no_mcp,
                    skip_grading=skip_grading,
                    without_skill_mode=without_skill_mode,
                    copy_ignore_prefixes=copy_ignore_prefixes,
                )

    baseline_config = "old_skill" if "old_skill" in resolved_configs else "without_skill"
    log("[3/4] Aggregating benchmark artefacts")
    benchmark = aggregate_iteration(
        repo_root=repo_root,
        skill_name=skill_name,
        iteration_dir=iteration_dir,
        model=model,
        baseline_config=baseline_config,
        mcp_enabled=not no_mcp,
    )
    write_json_file(iteration_dir / "benchmark.json", benchmark)
    write_benchmark_markdown(iteration_dir, benchmark, baseline_config)
    write_review_html(iteration_dir, benchmark)

    log("[4/4] Done")
    log(f"      benchmark.json: {iteration_dir / 'benchmark.json'}")
    log(f"      benchmark.md:   {iteration_dir / 'benchmark.md'}")
    log(f"      review.html:    {iteration_dir / 'review.html'}")
    return iteration_dir


def ensure_gh_auth() -> None:
    status = subprocess.run(
        ["gh", "auth", "status"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if status.returncode == 0:
        return
    raise SystemExit(
        "GitHub CLI authentication is required before running skill evals.\n"
        "Run `gh auth status` / `gh auth login` and try again.\n\n"
        f"stderr:\n{status.stderr.strip()}"
    )


def main() -> int:
    args = parse_args()
    repo_root = args.repo_root.resolve()
    workspace_root = args.workspace_root.resolve()
    validate_workspace_root(repo_root, workspace_root)
    skill_names = discover_skill_names(repo_root)
    requested_skill_names = skill_names if args.skill_name == "all" else [args.skill_name]
    unknown_skills = [skill_name for skill_name in requested_skill_names if skill_name not in skill_names]
    if unknown_skills:
        raise SystemExit(f"Unknown skill(s): {', '.join(unknown_skills)}")

    if args.report_only:
        log("[report] Regenerating workspace history and global overview reports from existing benchmarks")
    else:
        ensure_command_available("gh")
        ensure_gh_auth()
        for index, skill_name in enumerate(requested_skill_names, start=1):
            if len(requested_skill_names) > 1:
                log(f"=== Skill {index}/{len(requested_skill_names)}: {skill_name} ===")
            run_skill(
                repo_root=repo_root,
                workspace_root=workspace_root,
                skill_name=skill_name,
                eval_ids=args.eval_ids,
                configs=args.configs,
                runs_per_configuration=args.runs_per_configuration,
                model=args.model,
                timeout_seconds=args.timeout_seconds,
                force_iteration=args.force_iteration,
                mcp_config=args.mcp_config,
                no_mcp=args.no_mcp,
                skip_grading=args.skip_grading,
                without_skill_mode=args.without_skill_mode,
            )

    reports = refresh_workspace_and_global_reports(repo_root, workspace_root)
    log("[report] Workspace histories and global overview refreshed")
    log(f"         skills-overview.json: {reports['overview_json_path']}")
    log(f"         skills-overview.md:   {reports['overview_markdown_path']}")
    log(f"         skills-overview.html: {reports['overview_html_path']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())