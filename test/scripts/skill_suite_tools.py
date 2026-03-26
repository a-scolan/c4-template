from __future__ import annotations

import sys as _sys
from pathlib import Path as _Path

_SCRIPTS_DIR = str(_Path(__file__).resolve().parent)
if _SCRIPTS_DIR not in _sys.path:
    _sys.path.insert(0, _SCRIPTS_DIR)

"""Deterministic harness helpers for the benchmark custom-agent workflow."""

import argparse
import hashlib
import json
import os
import subprocess
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from benchmark.common import (
    calculate_benchmark_stats,
    coerce_bool,
    coerce_float,
    coerce_int,
    count_words,
    deep_copy_json_like,
    delta_or_none,
    file_sha256,
    iso_to_datetime,
    normalize_string_list,
    read_json,
    relative_to_root,
    round_or_none,
    safe_mean,
    utc_now_iso,
    write_json,
    write_text,
)
from benchmark.artifacts import (
    clean_benchmark_artifacts as _clean_benchmark_artifacts,
    prune_generated_artifacts as _prune_generated_artifacts,
)
from benchmark.evals import (
    load_split_eval_artifacts as _load_split_eval_artifacts,
    skill_eval_paths as _skill_eval_paths,
    skill_eval_root as _skill_eval_root,
    validate_grading_spec_definition as _validate_grading_spec_definition,
    validate_public_eval_definition as _validate_public_eval_definition,
    validate_split_eval_pair as _validate_split_eval_pair,
    validate_workspace_eval_artifacts as _validate_workspace_eval_artifacts,
    workspace_benchmark_skill_names as _workspace_benchmark_skill_names,
)
from benchmark.metrics import (
    build_run_metrics_payload as _build_run_metrics_payload,
    canonicalize_run_metrics as _canonicalize_run_metrics,
    extract_files_read_count as _extract_files_read_count,
    extract_timestamp_field as _extract_timestamp_field,
    infer_run_metrics_fields as _infer_run_metrics_fields,
    load_run_metrics as _load_run_metrics,
    parse_eval_metrics_path as _parse_eval_metrics_path,
    validate_run_metrics_payload as _validate_run_metrics_payload,
)
from benchmark.protocol import (
    build_protocol_manifest as _build_protocol_manifest,
    freeze_protocol_for_iteration as _freeze_protocol_for_iteration,
    protocol_manifest_path as _protocol_manifest_path,
    validate_protocol_manifest as _validate_protocol_manifest,
)
from benchmark.rendering import (
    format_number as _format_number,
    markdown_table as _markdown_table,
    render_markdown as _render_markdown,
)


ITERATION_RE = re.compile(r"^iteration-(\d+)$")
SERIES_ITERATION_RE = re.compile(r"^(.+?-test)(\d+)?$")
RUN_DIR_RE = re.compile(r"^run-(\d+)$")
EVAL_METRICS_RE = re.compile(r"^eval-(\d+)-metrics$")
WORD_RE = re.compile(r"\S+")

EVAL_ARTIFACT_SCHEMA_VERSION = 2
COMPARATOR_SCHEMA_VERSION = 2
BENCHMARK_PROTOCOL_VERSION = "benchmark-v3"
EVALS_PUBLIC_FILENAME = "evals-public.json"
GRADING_SPEC_FILENAME = "grading-spec.json"
ITERATION_CAVEATS_FILENAME = "benchmark-caveats.json"
COMPARATOR_SIDES = ("A", "B")
COMPARATOR_WINNERS = {"A", "B", "TIE"}
PROTOCOL_MANIFEST_RELATIVE_PATH = Path("test") / "benchmark-protocol.json"
PROTOCOL_TRACKED_FILES = (
    ".github/agents/skill-benchmark-manager.agent.md",
    ".github/agents/skill-benchmark-baseline.agent.md",
    ".github/agents/skill-benchmark-baseline-hook-only.agent.md",
    ".github/agents/skill-benchmark-with-skill.agent.md",
    ".github/agents/skill-blind-comparator.agent.md",
    "test/scripts/benchmark_access_hook.py",
    "test/benchmark-agent-workflow.md",
    "test/scripts/skill_suite_tools.py",
)
HOOK_DEBUG_LOG_RELATIVE_PATH = Path("test") / "_agent-hooks" / "hook-debug.jsonl"
HOOK_AUDIT_LOG_RELATIVE_PATH = Path("test") / "_agent-hooks" / "hook-audit.jsonl"
HOOK_STATE_FILENAME_RE = re.compile(r"[^A-Za-z0-9_.-]+")
ANONYMOUS_HOOK_SESSION_PREFIX = "anonymous-"
BENCH_HOOK_MODES = (
    "benchmark_manager",
    "baseline",
    "baseline_hook_only",
    "with_skill_targeted",
    "blind_compare",
)
STATEFUL_ANONYMOUS_HOOK_MODES = {"with_skill_targeted", "blind_compare"}
RESTRICTED_LIKEC4_MCP_NORMALIZED_NAMES = {
    "mcplikec4listprojects",
    "mcplikec4readprojectsummary",
    "mcplikec4readview",
    "mcplikec4openview",
}
HOOK_AUDIT_ALLOWED_READ_PREFIXES = {
    "baseline": ("projects/shared/",),
    "baseline_hook_only": ("projects/shared/",),
    "with_skill_targeted": ("projects/shared/", ".github/skills/"),
}
HIGH_VARIANCE_EXPECTATION_STDDEV = 0.2
HIGH_VARIANCE_RUBRIC_STDDEV = 1.0

BENCHMARK_AGENTS = {
    "manager": "Skill Benchmark Manager",
    "without_skill": "Skill Benchmark Baseline",
    "without_skill_hook_only": "Skill Benchmark Baseline Hook-Only",
    "with_skill": "Skill Benchmark With Skill",
    "blind_compare": "Skill Blind Comparator",
}
INTERACTIVE_ENTRYPOINT = BENCHMARK_AGENTS["manager"]
AUTOMATION_ENTRYPOINT = "python test/scripts/skill_suite_tools.py self-test --iteration test/iteration-N --workspace-root ."
BLIND_FORBIDDEN_TOKENS = [
    "blind-map.json",
    "with_skill/response.md",
    "without_skill/response.md",
    "with_skill-summary.json",
    "without_skill-summary.json",
    "with_skill-run-metrics.json",
    "without_skill-run-metrics.json",
    "SKILL.md",
]
REQUIRED_RUN_METRIC_KEYS = (
    "skill_name",
    "configuration",
    "language",
    "mcp_used",
    "started_at",
    "finished_at",
    "elapsed_seconds_total",
    "files_read_count",
    "files_written_count",
)
RUN_METRIC_KEY_ALIASES = {
    "skill_name": ("skill_name",),
    "configuration": ("configuration",),
    "language": ("language",),
    "mcp_used": ("mcp_used",),
    "started_at": ("started_at", "started_at_utc", "start_timestamp_utc"),
    "finished_at": ("finished_at", "finished_at_utc", "finish_timestamp_utc"),
    "elapsed_seconds_total": ("elapsed_seconds_total",),
    "files_read_count": ("files_read_count", "intentionally_read_workspace_files_count", "workspace_files_intentionally_read"),
    "files_written_count": (
        "files_written_count",
        "files_written_under_target_output_dir_count",
        "files_written_under_target_output_directory_count",
    ),
}
RUN_METRIC_LIST_FALLBACKS = {
    "files_read_count": ("intentionally_read_workspace_files", "workspace_files_read"),
    "files_written_count": (
        "files_written_under_target_output_dir",
        "files_written_under_target_output_directory",
        "files_written",
    ),
}
RUN_METRIC_DEFAULTS = {
    "language": "English",
    "mcp_used": False,
}
RUN_METRIC_ALIAS_KEYS_TO_DROP = {
    alias
    for key, aliases in RUN_METRIC_KEY_ALIASES.items()
    for alias in aliases
    if alias != key
}


def anonymous_hook_session_id(mode: str) -> str:
    return f"{ANONYMOUS_HOOK_SESSION_PREFIX}{mode}"


def hook_state_root(workspace_root: Path) -> Path:
    return workspace_root / "test" / "_agent-hooks"


def hook_state_path(workspace_root: Path, session_id: str) -> Path:
    safe_name = HOOK_STATE_FILENAME_RE.sub("_", session_id or "default")
    return hook_state_root(workspace_root) / f"{safe_name}.json"


def hook_state_reset_candidates(mode: str | None = None, session_id: str | None = None) -> list[str]:
    candidates: list[str] = []
    if isinstance(session_id, str) and session_id.strip():
        candidates.append(session_id.strip())
    elif isinstance(mode, str) and mode.strip():
        normalized_mode = mode.strip()
        candidates.append(anonymous_hook_session_id(normalized_mode))
        if normalized_mode in STATEFUL_ANONYMOUS_HOOK_MODES:
            candidates.append("default")
    else:
        candidates.append("default")

    ordered: list[str] = []
    seen: set[str] = set()
    for candidate in candidates:
        if candidate not in seen:
            seen.add(candidate)
            ordered.append(candidate)
    return ordered


def reset_hook_state(workspace_root: Path, *, mode: str | None = None, session_id: str | None = None) -> dict[str, Any]:
    state_root = hook_state_root(workspace_root)
    state_root.mkdir(parents=True, exist_ok=True)

    removed: list[str] = []
    missing: list[str] = []
    resolved_sessions = hook_state_reset_candidates(mode, session_id)
    if not session_id and isinstance(mode, str) and mode.strip() in STATEFUL_ANONYMOUS_HOOK_MODES:
        anonymous_prefix = anonymous_hook_session_id(mode.strip())
        for candidate in sorted(state_root.glob(f"{anonymous_prefix}*.json"), key=lambda path: path.name):
            resolved_session_id = candidate.stem
            if resolved_session_id not in resolved_sessions:
                resolved_sessions.append(resolved_session_id)

    for resolved_session_id in resolved_sessions:
        state_path = hook_state_path(workspace_root, resolved_session_id)
        relative_path = state_path.relative_to(workspace_root).as_posix()
        if state_path.exists():
            state_path.unlink()
            removed.append(relative_path)
        else:
            missing.append(relative_path)

    return {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "workspace_root": workspace_root.as_posix(),
        "mode": mode,
        "session_id": session_id,
        "resolved_session_ids": resolved_sessions,
        "removed_count": len(removed),
        "removed": removed,
        "missing_count": len(missing),
        "missing": missing,
    }


def skill_eval_root(workspace_root: Path, skill_name: str) -> Path:
    return _skill_eval_root(workspace_root, skill_name)


def skill_eval_paths(workspace_root: Path, skill_name: str) -> dict[str, Path]:
    return _skill_eval_paths(workspace_root, skill_name, EVALS_PUBLIC_FILENAME, GRADING_SPEC_FILENAME)


def workspace_benchmark_skill_names(workspace_root: Path) -> list[str]:
    return _workspace_benchmark_skill_names(workspace_root, EVALS_PUBLIC_FILENAME, GRADING_SPEC_FILENAME)


def validate_public_eval_definition(skill_name: str, data: dict[str, Any]) -> list[str]:
    return _validate_public_eval_definition(skill_name, data)


def validate_grading_spec_definition(skill_name: str, data: dict[str, Any]) -> list[str]:
    return _validate_grading_spec_definition(skill_name, data)


def validate_split_eval_pair(skill_name: str, public: dict[str, Any], grading: dict[str, Any]) -> list[str]:
    return _validate_split_eval_pair(skill_name, public, grading)


def load_split_eval_artifacts(workspace_root: Path, skill_name: str) -> dict[str, Any]:
    return _load_split_eval_artifacts(workspace_root, skill_name, EVALS_PUBLIC_FILENAME, GRADING_SPEC_FILENAME)


def validate_workspace_eval_artifacts(workspace_root: Path) -> dict[str, Any]:
    return _validate_workspace_eval_artifacts(workspace_root, EVALS_PUBLIC_FILENAME, GRADING_SPEC_FILENAME)


def protocol_manifest_path(workspace_root: Path, manifest_path: Path | None = None) -> Path:
    return _protocol_manifest_path(workspace_root, PROTOCOL_MANIFEST_RELATIVE_PATH, manifest_path)


def build_protocol_manifest(workspace_root: Path, version: str = BENCHMARK_PROTOCOL_VERSION) -> dict[str, Any]:
    return _build_protocol_manifest(
        workspace_root,
        version=version,
        tracked_files=PROTOCOL_TRACKED_FILES,
        eval_artifact_schema_version=EVAL_ARTIFACT_SCHEMA_VERSION,
        comparator_schema_version=COMPARATOR_SCHEMA_VERSION,
    )


def validate_protocol_manifest(workspace_root: Path, manifest_path: Path) -> dict[str, Any]:
    return _validate_protocol_manifest(workspace_root, manifest_path)


def freeze_protocol_for_iteration(iteration_dir: Path, workspace_root: Path, manifest_path: Path) -> dict[str, Any]:
    return _freeze_protocol_for_iteration(
        iteration_dir,
        workspace_root,
        manifest_path,
        evals_public_filename=EVALS_PUBLIC_FILENAME,
        grading_spec_filename=GRADING_SPEC_FILENAME,
    )


def run_label(run_number: int) -> str:
    return f"run-{run_number}"


def response_run_dir(skill_dir: Path, eval_id: int, configuration: str, run_number: int) -> Path:
    return skill_dir / f"eval-{eval_id}" / configuration / run_label(run_number)


def response_path_for_run(skill_dir: Path, eval_id: int, configuration: str, run_number: int) -> Path:
    return response_run_dir(skill_dir, eval_id, configuration, run_number) / "response.md"


def legacy_response_path(skill_dir: Path, eval_id: int, configuration: str) -> Path:
    return skill_dir / f"eval-{eval_id}" / configuration / "response.md"


def resolve_response_path(skill_dir: Path, eval_id: int, configuration: str, run_number: int) -> Path | None:
    run_path = response_path_for_run(skill_dir, eval_id, configuration, run_number)
    if run_path.exists():
        return run_path
    flat_path = legacy_response_path(skill_dir, eval_id, configuration)
    if run_number == 1 and flat_path.exists():
        return flat_path
    return None


def blind_dir_for_run(eval_dir: Path, run_number: int) -> Path:
    return eval_dir / "blind" / run_label(run_number)


def legacy_blind_dir(eval_dir: Path) -> Path:
    return eval_dir / "blind"


def blind_map_path(eval_dir: Path, run_number: int) -> Path:
    return eval_dir / f"blind-map.{run_label(run_number)}.json"


def resolve_blind_dir(eval_dir: Path, run_number: int) -> Path | None:
    run_dir = blind_dir_for_run(eval_dir, run_number)
    if (run_dir / "A.md").exists() and (run_dir / "B.md").exists():
        return run_dir
    return None


def per_run_metrics_dir(skill_dir: Path, configuration: str) -> Path:
    return skill_dir / "_runs" / configuration


def per_run_metrics_path(skill_dir: Path, configuration: str, run_number: int) -> Path:
    return per_run_metrics_dir(skill_dir, configuration) / f"{run_label(run_number)}-metrics.json"


def per_eval_run_metrics_dir(skill_dir: Path, configuration: str, run_number: int) -> Path:
    return per_run_metrics_dir(skill_dir, configuration) / run_label(run_number)


def per_eval_run_metrics_path(skill_dir: Path, configuration: str, eval_id: int, run_number: int) -> Path:
    return per_eval_run_metrics_dir(skill_dir, configuration, run_number) / f"eval-{eval_id}-metrics.json"


def parse_eval_metrics_path(path: Path) -> int | None:
    return _parse_eval_metrics_path(path, EVAL_METRICS_RE)


def discover_run_numbers(skill_dir: Path, configuration: str) -> list[int]:
    discovered: set[int] = set()
    metrics_root = per_run_metrics_dir(skill_dir, configuration)
    if metrics_root.exists():
        for child in metrics_root.glob("run-*-metrics.json"):
            match = RUN_DIR_RE.match(child.stem.replace("-metrics", ""))
            if match:
                discovered.add(int(match.group(1)))
        for child in metrics_root.iterdir():
            if not child.is_dir():
                continue
            match = RUN_DIR_RE.match(child.name)
            if match and any(parse_eval_metrics_path(path) is not None for path in child.glob("eval-*-metrics.json")):
                discovered.add(int(match.group(1)))

    for eval_dir in sorted(skill_dir.glob("eval-*"), key=lambda path: path.name):
        flat_response = legacy_response_path(skill_dir, int(eval_dir.name.split("-", 1)[1]), configuration)
        if flat_response.exists():
            discovered.add(1)
        config_dir = eval_dir / configuration
        if config_dir.exists():
            for child in config_dir.iterdir():
                if not child.is_dir():
                    continue
                match = RUN_DIR_RE.match(child.name)
                if match and (child / "response.md").exists():
                    discovered.add(int(match.group(1)))
    return sorted(discovered) or [1]


def extract_timestamp_field(payload: dict[str, Any], *keys: str) -> str | None:
    return _extract_timestamp_field(payload, *keys)


def extract_files_read_count(payload: dict[str, Any]) -> int:
    return _extract_files_read_count(payload)


def refresh_run_metrics_collection(skill_dir: Path, configuration: str) -> dict[str, Any]:
    run_metrics_root = per_run_metrics_dir(skill_dir, configuration)
    run_metrics_root.mkdir(parents=True, exist_ok=True)

    run_numbers = discover_run_numbers(skill_dir, configuration)
    if not run_numbers:
        raise FileNotFoundError(f"No per-run metrics found for {skill_dir.name} {configuration}: {run_metrics_root}")

    runs: list[dict[str, Any]] = []
    elapsed_values: list[float] = []
    files_read_values: list[float] = []
    files_written_values: list[float] = []
    for run_number in run_numbers:
        per_eval_paths = sorted(
            [
                path
                for path in per_eval_run_metrics_dir(skill_dir, configuration, run_number).glob("eval-*-metrics.json")
                if parse_eval_metrics_path(path) is not None
            ],
            key=lambda path: parse_eval_metrics_path(path) or -1,
        )

        if per_eval_paths:
            eval_metrics: list[dict[str, Any]] = []
            started_candidates: list[datetime] = []
            finished_candidates: list[datetime] = []
            elapsed_total = 0.0
            files_read_total = 0
            files_written_total = 0
            languages: list[str] = []
            mcp_used = False

            for path in per_eval_paths:
                metrics, _changes = load_run_metrics(path, write_back=True)
                missing_keys = validate_run_metrics_payload(metrics)
                if missing_keys:
                    raise ValueError(
                        f"Incomplete per-eval run metrics for {skill_dir.name} {configuration} run-{run_number}: missing/null keys {missing_keys} in {path}"
                    )

                eval_id = parse_eval_metrics_path(path)
                eval_metrics.append(
                    {
                        "eval_id": eval_id,
                        "path": path.relative_to(skill_dir).as_posix(),
                        **metrics,
                    }
                )

                started_at = iso_to_datetime(metrics.get("started_at"))
                finished_at = iso_to_datetime(metrics.get("finished_at"))
                if started_at is not None:
                    started_candidates.append(started_at)
                if finished_at is not None:
                    finished_candidates.append(finished_at)

                elapsed_total += float(metrics.get("elapsed_seconds_total", 0.0) or 0.0)
                files_read_total += int(metrics.get("files_read_count", 0) or 0)
                files_written_total += int(metrics.get("files_written_count", 0) or 0)

                if isinstance(metrics.get("language"), str) and metrics.get("language", "").strip():
                    languages.append(metrics["language"].strip())
                mcp_used = mcp_used or bool(metrics.get("mcp_used", False))

            started_at = min(started_candidates).strftime("%Y-%m-%dT%H:%M:%SZ") if started_candidates else utc_now_iso()
            finished_at = max(finished_candidates).strftime("%Y-%m-%dT%H:%M:%SZ") if finished_candidates else utc_now_iso()
            normalized = build_run_metrics_payload(
                skill_name=skill_dir.name,
                configuration=configuration,
                language=languages[0] if languages else "English",
                mcp_used=mcp_used,
                started_at=started_at,
                finished_at=finished_at,
                elapsed_seconds_total=round(elapsed_total, 6),
                files_read_count=files_read_total,
                files_written_count=files_written_total,
                run_number=run_number,
            )
            normalized["worker_count"] = len(per_eval_paths)
            normalized["eval_metrics"] = eval_metrics
        else:
            path = per_run_metrics_path(skill_dir, configuration, run_number)
            metrics, _changes = load_run_metrics(path, write_back=True)
            normalized = dict(metrics)
            normalized["run_number"] = run_number

        normalized, _changes = canonicalize_run_metrics(normalized)
        missing_keys = validate_run_metrics_payload(normalized)
        if missing_keys:
            raise ValueError(
                f"Incomplete normalized run metrics for {skill_dir.name} {configuration} run-{run_number}: missing/null keys {missing_keys}"
            )

        runs.append(normalized)
        elapsed = coerce_float(normalized.get("elapsed_seconds_total"))
        if elapsed is not None:
            elapsed_values.append(elapsed)
        files_read = coerce_float(normalized.get("files_read_count"))
        if files_read is not None:
            files_read_values.append(files_read)
        files_written = coerce_float(normalized.get("files_written_count"))
        if files_written is not None:
            files_written_values.append(files_written)

    first_run = runs[0]
    started_candidates = [iso_to_datetime(run.get("started_at")) for run in runs]
    finished_candidates = [iso_to_datetime(run.get("finished_at")) for run in runs]
    started_at = min((value for value in started_candidates if value is not None), default=None)
    finished_at = max((value for value in finished_candidates if value is not None), default=None)

    collection = {
        "skill_name": first_run.get("skill_name", skill_dir.name),
        "configuration": first_run.get("configuration", configuration),
        "language": first_run.get("language", "English"),
        "mcp_used": any(bool(run.get("mcp_used", False)) for run in runs),
        "started_at": started_at.strftime("%Y-%m-%dT%H:%M:%SZ") if started_at else first_run.get("started_at"),
        "finished_at": finished_at.strftime("%Y-%m-%dT%H:%M:%SZ") if finished_at else first_run.get("finished_at"),
        "elapsed_seconds_total": first_run.get("elapsed_seconds_total"),
        "files_read_count": first_run.get("files_read_count"),
        "files_written_count": first_run.get("files_written_count"),
        "run_count": len(runs),
        "runs": runs,
        "aggregate": {
            "elapsed_seconds_total": calculate_benchmark_stats(elapsed_values) if elapsed_values else None,
            "files_read_count": calculate_benchmark_stats(files_read_values) if files_read_values else None,
            "files_written_count": calculate_benchmark_stats(files_written_values) if files_written_values else None,
        },
    }
    collection, _changes = canonicalize_run_metrics(collection)
    collection_missing_keys = validate_run_metrics_payload(collection)
    if collection_missing_keys:
        raise ValueError(
            f"Incomplete consolidated run metrics for {skill_dir.name} {configuration}: missing/null keys {collection_missing_keys}"
        )
    output_path = skill_dir / f"{configuration}-run-metrics.json"
    write_json(output_path, collection)
    return collection


def validate_comparison_side_payload(side_label: str, payload: Any) -> list[str]:
    issues: list[str] = []
    if not isinstance(payload, dict):
        return [f"comparison side {side_label} must be an object"]

    overall_score = coerce_float(payload.get("overall_score"))
    if overall_score is None:
        issues.append(f"comparison side {side_label} must provide numeric rubric.{side_label}.overall_score")
    elif not 0.0 <= overall_score <= 10.0:
        issues.append(f"comparison side {side_label} overall_score must be on the 0-10 scale")

    content_score = coerce_float(payload.get("content_score"))
    if content_score is None:
        issues.append(f"comparison side {side_label} must provide numeric rubric.{side_label}.content_score")
    elif not 0.0 <= content_score <= 10.0:
        issues.append(f"comparison side {side_label} content_score must be on the 0-10 scale")

    structure_score = coerce_float(payload.get("structure_score"))
    if structure_score is None:
        issues.append(f"comparison side {side_label} must provide numeric rubric.{side_label}.structure_score")
    elif not 0.0 <= structure_score <= 10.0:
        issues.append(f"comparison side {side_label} structure_score must be on the 0-10 scale")

    notes = payload.get("notes")
    if notes is not None and (not isinstance(notes, str) or not notes.strip()):
        issues.append(f"comparison side {side_label} notes must be a non-empty string when provided")
    return issues


def validate_expectation_side_payload(side_label: str, payload: Any) -> list[str]:
    issues: list[str] = []
    if not isinstance(payload, dict):
        return [f"expectation_results.{side_label} must be an object"]

    passed = coerce_int(payload.get("passed"))
    total = coerce_int(payload.get("total"))
    pass_rate = coerce_float(payload.get("pass_rate"))
    if passed is None or passed < 0:
        issues.append(f"expectation_results.{side_label}.passed must be a non-negative integer")
    if total is None or total < 0:
        issues.append(f"expectation_results.{side_label}.total must be a non-negative integer")
    if pass_rate is None or not 0.0 <= pass_rate <= 1.0:
        issues.append(f"expectation_results.{side_label}.pass_rate must be a number between 0 and 1")
    if passed is not None and total is not None and total < passed:
        issues.append(f"expectation_results.{side_label}.total must be >= passed")
    if passed is not None and total is not None and pass_rate is not None:
        expected_rate = 0.0 if total == 0 else (passed / total)
        if abs(expected_rate - float(pass_rate)) > 0.005:
            issues.append(f"expectation_results.{side_label}.pass_rate must equal passed / total")
    return issues


def normalize_comparison_entry(raw_entry: Any) -> dict[str, Any]:
    if not isinstance(raw_entry, dict):
        raise ValueError("Each comparison entry must be a JSON object")

    normalized = deep_copy_json_like(raw_entry)
    normalized["schema_version"] = COMPARATOR_SCHEMA_VERSION
    normalized["run_number"] = coerce_int(normalized.get("run_number")) or 1

    issues: list[str] = []
    eval_id = normalized.get("eval_id")
    if not isinstance(eval_id, int):
        issues.append("comparison entry must provide an integer eval_id")

    winner = normalized.get("winner")
    if winner not in COMPARATOR_WINNERS:
        issues.append("comparison winner must be one of A, B, or TIE")

    reasoning = normalized.get("reasoning")
    if not isinstance(reasoning, str) or not reasoning.strip():
        issues.append("comparison reasoning must be a non-empty string")

    rubric = normalized.get("rubric")
    if not isinstance(rubric, dict):
        issues.append("comparison rubric must be an object")
    else:
        for side in COMPARATOR_SIDES:
            issues.extend(validate_comparison_side_payload(side, rubric.get(side)))

    expectation_results = normalized.get("expectation_results")
    if not isinstance(expectation_results, dict):
        issues.append("comparison expectation_results must be an object")
    else:
        for side in COMPARATOR_SIDES:
            issues.extend(validate_expectation_side_payload(side, expectation_results.get(side)))

    if issues:
        raise ValueError("; ".join(issues))

    return normalized


def materialize_run_artifacts(
    iteration_dir: Path,
    skill_name: str,
    configuration: str,
    raw_json_path: Path,
    *,
    run_number: int = 1,
    started_at: str | None = None,
    finished_at: str | None = None,
) -> dict[str, Any]:
    raw = read_json(raw_json_path)
    if not isinstance(raw, dict):
        raise ValueError(f"Expected a JSON object in {raw_json_path}")

    raw_skill_name = raw.get("skill_name")
    if isinstance(raw_skill_name, str) and raw_skill_name.strip() and raw_skill_name != skill_name:
        raise ValueError(
            f"Raw payload skill_name mismatch: expected '{skill_name}', got '{raw_skill_name}'"
        )

    raw_configuration = raw.get("configuration")
    if isinstance(raw_configuration, str) and raw_configuration.strip() and raw_configuration != configuration:
        raise ValueError(
            f"Raw payload configuration mismatch: expected '{configuration}', got '{raw_configuration}'"
        )

    responses = raw.get("responses")
    if not isinstance(responses, list) or not responses:
        raise ValueError(f"Raw payload {raw_json_path} must contain a non-empty 'responses' list")

    skill_dir = iteration_dir / skill_name
    response_ids: set[int] = set()
    written_files: list[str] = []
    for item in responses:
        if not isinstance(item, dict):
            raise ValueError(f"Each response entry must be an object in {raw_json_path}")
        eval_id = item.get("id")
        if not isinstance(eval_id, int):
            raise ValueError(f"Each response entry must contain an integer 'id' in {raw_json_path}")
        if eval_id in response_ids:
            raise ValueError(f"Duplicate eval id {eval_id} in {raw_json_path}")
        response_ids.add(eval_id)

        response = item.get("response")
        if not isinstance(response, str) or not response.strip():
            raise ValueError(f"Eval {eval_id} in {raw_json_path} must contain a non-empty 'response' string")

        output_path = response_path_for_run(skill_dir, eval_id, configuration, run_number)
        write_text(output_path, response.rstrip() + "\n")
        written_files.append(output_path.relative_to(iteration_dir).as_posix())

        if run_number == 1:
            flat_output_path = legacy_response_path(skill_dir, eval_id, configuration)
            write_text(flat_output_path, response.rstrip() + "\n")
            if flat_output_path != output_path:
                written_files.append(flat_output_path.relative_to(iteration_dir).as_posix())

    started_value = started_at or extract_timestamp_field(
        raw,
        "started_at",
        "started_at_utc",
        "start_timestamp_utc",
    )
    finished_value = finished_at or extract_timestamp_field(
        raw,
        "finished_at",
        "finished_at_utc",
        "finish_timestamp_utc",
    )
    if not started_value or not finished_value:
        raise ValueError(
            f"Raw payload {raw_json_path} must provide started_at/finished_at (or compatible aliases), or they must be passed via CLI"
        )

    language = raw.get("language") if isinstance(raw.get("language"), str) and raw.get("language").strip() else "English"
    mcp_used_value = coerce_bool(raw.get("mcp_used"))
    mcp_used = bool(mcp_used_value) if mcp_used_value is not None else False
    files_read_count = extract_files_read_count(raw)

    started_dt = iso_to_datetime(started_value)
    finished_dt = iso_to_datetime(finished_value)
    if not started_dt or not finished_dt:
        raise ValueError(
            f"Invalid started_at/finished_at values in {raw_json_path}: {started_value!r}, {finished_value!r}"
        )
    elapsed_seconds_total = round((finished_dt - started_dt).total_seconds(), 6)
    if elapsed_seconds_total < 0:
        raise ValueError(f"finished_at precedes started_at in {raw_json_path}")

    metrics_payload = build_run_metrics_payload(
        skill_name=skill_name,
        configuration=configuration,
        language=language,
        mcp_used=mcp_used,
        started_at=started_value,
        finished_at=finished_value,
        elapsed_seconds_total=elapsed_seconds_total,
        files_read_count=files_read_count,
        files_written_count=len(written_files),
        run_number=run_number,
    )
    per_eval_metrics_output = None
    if len(response_ids) == 1:
        eval_id = next(iter(response_ids))
        metrics_payload["eval_id"] = eval_id
        run_metrics_path = per_eval_run_metrics_path(skill_dir, configuration, eval_id, run_number)
        per_eval_metrics_output = str(run_metrics_path)
    else:
        run_metrics_path = per_run_metrics_path(skill_dir, configuration, run_number)
    write_json(run_metrics_path, metrics_payload)
    collection = refresh_run_metrics_collection(skill_dir, configuration)

    return {
        "iteration": iteration_dir.name,
        "skill_name": skill_name,
        "configuration": configuration,
        "run_number": run_number,
        "raw_json": str(raw_json_path),
        "responses_written": len(written_files),
        "written_files": written_files,
        "run_metrics_path": str(skill_dir / f"{configuration}-run-metrics.json"),
        "per_run_metrics_path": str(run_metrics_path),
        "per_eval_metrics_path": per_eval_metrics_output,
        "run_count": collection.get("run_count", 1),
        "files_read_count": files_read_count,
        "elapsed_seconds_total": elapsed_seconds_total,
    }


def materialize_blind_comparisons(iteration_dir: Path, skill_name: str, raw_json_path: Path) -> dict[str, Any]:
    raw = read_json(raw_json_path)
    if isinstance(raw, dict):
        raw_skill_name = raw.get("skill_name")
        if isinstance(raw_skill_name, str) and raw_skill_name.strip() and raw_skill_name != skill_name:
            raise ValueError(
                f"Raw payload skill_name mismatch: expected '{skill_name}', got '{raw_skill_name}'"
            )
        comparisons = raw.get("comparisons")
    elif isinstance(raw, list):
        comparisons = raw
    else:
        raise ValueError(f"Expected a JSON object or list in {raw_json_path}")

    if not isinstance(comparisons, list):
        raise ValueError(f"Raw payload {raw_json_path} must contain a 'comparisons' list")

    normalized_comparisons = [normalize_comparison_entry(item) for item in comparisons]

    output_path = iteration_dir / skill_name / "blind-comparisons.json"
    write_json(
        output_path,
        {
            "schema_version": COMPARATOR_SCHEMA_VERSION,
            "skill_name": skill_name,
            "comparisons": normalized_comparisons,
        },
    )
    return {
        "iteration": iteration_dir.name,
        "skill_name": skill_name,
        "raw_json": str(raw_json_path),
        "comparison_count": len(normalized_comparisons),
        "output_path": str(output_path),
    }


def infer_run_metrics_fields(metrics_path: Path) -> dict[str, str | None]:
    return _infer_run_metrics_fields(metrics_path)


def build_run_metrics_payload(
    *,
    skill_name: str,
    configuration: str,
    language: str,
    mcp_used: bool,
    started_at: str,
    finished_at: str,
    elapsed_seconds_total: float,
    files_read_count: int,
    files_written_count: int,
    run_number: int | None = None,
) -> dict[str, Any]:
    return _build_run_metrics_payload(
        skill_name=skill_name,
        configuration=configuration,
        language=language,
        mcp_used=mcp_used,
        started_at=started_at,
        finished_at=finished_at,
        elapsed_seconds_total=elapsed_seconds_total,
        files_read_count=files_read_count,
        files_written_count=files_written_count,
        run_number=run_number,
    )


def canonicalize_run_metrics(metrics: dict[str, Any], metrics_path: Path | None = None) -> tuple[dict[str, Any], list[str]]:
    return _canonicalize_run_metrics(
        metrics,
        metrics_path,
        required_run_metric_keys=REQUIRED_RUN_METRIC_KEYS,
        run_metric_key_aliases=RUN_METRIC_KEY_ALIASES,
        run_metric_list_fallbacks=RUN_METRIC_LIST_FALLBACKS,
        run_metric_defaults=RUN_METRIC_DEFAULTS,
        run_metric_alias_keys_to_drop=RUN_METRIC_ALIAS_KEYS_TO_DROP,
    )


def load_run_metrics(metrics_path: Path, *, write_back: bool) -> tuple[dict[str, Any], list[str]]:
    return _load_run_metrics(
        metrics_path,
        write_back=write_back,
        required_run_metric_keys=REQUIRED_RUN_METRIC_KEYS,
        run_metric_key_aliases=RUN_METRIC_KEY_ALIASES,
        run_metric_list_fallbacks=RUN_METRIC_LIST_FALLBACKS,
        run_metric_defaults=RUN_METRIC_DEFAULTS,
        run_metric_alias_keys_to_drop=RUN_METRIC_ALIAS_KEYS_TO_DROP,
    )


def iteration_number(path: Path) -> int | None:
    match = ITERATION_RE.match(path.name)
    return int(match.group(1)) if match else None


def iteration_series_key(path: Path) -> tuple[str, int] | None:
    name = path.name
    iteration_match = ITERATION_RE.match(name)
    if iteration_match:
        return ("iteration", int(iteration_match.group(1)))

    series_match = SERIES_ITERATION_RE.match(name)
    if series_match:
        series_name = series_match.group(1)
        series_number = int(series_match.group(2) or "1")
        return (series_name, series_number)

    return None


def workspace_skills_root(workspace_root: Path) -> Path:
    return workspace_root / ".github" / "skills"


def disabled_skills_root(iteration_dir: Path) -> Path:
    return iteration_dir / "_disabled-skills"


def disable_workspace_skills(workspace_root: Path, iteration_dir: Path) -> dict[str, Any]:
    skills_root = workspace_skills_root(workspace_root)
    disabled_root = disabled_skills_root(iteration_dir)
    manifest_path = iteration_dir / "_meta" / "skills-relocation.json"

    skills_root.mkdir(parents=True, exist_ok=True)
    disabled_root.mkdir(parents=True, exist_ok=True)

    existing_backups = [child.name for child in disabled_root.iterdir() if child.is_dir()]
    if existing_backups:
        raise FileExistsError(
            f"Disabled skills backup directory is not empty: {disabled_root}"
        )

    moved: list[dict[str, str]] = []
    for child in sorted(skills_root.iterdir(), key=lambda path: path.name):
        if not child.is_dir():
            continue
        destination = disabled_root / child.name
        child.rename(destination)
        moved.append(
            {
                "skill": child.name,
                "from": relative_to_root(skills_root / child.name, workspace_root),
                "to": relative_to_root(destination, workspace_root),
            }
        )

    summary = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "operation": "disable-workspace-skills",
        "skills_root": relative_to_root(skills_root, workspace_root),
        "disabled_root": relative_to_root(disabled_root, workspace_root),
        "moved_count": len(moved),
        "moved": moved,
    }
    write_json(manifest_path, summary)
    return summary


def restore_workspace_skills(workspace_root: Path, iteration_dir: Path) -> dict[str, Any]:
    skills_root = workspace_skills_root(workspace_root)
    disabled_root = disabled_skills_root(iteration_dir)
    manifest_path = iteration_dir / "_meta" / "skills-relocation.json"
    restore_path = iteration_dir / "_meta" / "skills-restoration.json"

    if not manifest_path.exists():
        raise FileNotFoundError(f"Missing relocation manifest: {manifest_path}")

    manifest = read_json(manifest_path)
    skills_root.mkdir(parents=True, exist_ok=True)
    disabled_root.mkdir(parents=True, exist_ok=True)

    restored: list[dict[str, str]] = []
    for item in manifest.get("moved", []):
        skill_name = item["skill"]
        source = disabled_root / skill_name
        destination = skills_root / skill_name
        if not source.exists():
            raise FileNotFoundError(f"Missing disabled skill backup for {skill_name}: {source}")
        if destination.exists():
            raise FileExistsError(f"Cannot restore {skill_name}; destination already exists: {destination}")
        try:
            source.rename(destination)
        except PermissionError:
            shutil.copytree(source, destination)
            shutil.rmtree(source)
        restored.append(
            {
                "skill": skill_name,
                "from": relative_to_root(source, workspace_root),
                "to": relative_to_root(destination, workspace_root),
            }
        )

    summary = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "operation": "restore-workspace-skills",
        "skills_root": relative_to_root(skills_root, workspace_root),
        "disabled_root": relative_to_root(disabled_root, workspace_root),
        "restored_count": len(restored),
        "restored": restored,
    }
    write_json(restore_path, summary)
    return summary


def find_previous_iteration(test_root: Path, current_iteration: Path) -> Path | None:
    current_series = iteration_series_key(current_iteration)
    if current_series is None:
        return None

    current_family, current_number = current_series
    candidates: list[tuple[int, Path]] = []
    for child in test_root.iterdir():
        if not child.is_dir():
            continue
        series = iteration_series_key(child)
        if series is None:
            continue
        family, number = series
        if family != current_family:
            continue
        if number < current_number:
            candidates.append((number, child))
    if not candidates:
        return None
    candidates.sort(key=lambda item: item[0])
    return candidates[-1][1]


def skill_dirs(iteration_dir: Path) -> list[Path]:
    return sorted(
        [
            child
            for child in iteration_dir.iterdir()
            if child.is_dir() and not child.name.startswith("_") and child.name != "scripts"
        ],
        key=lambda path: path.name,
    )


def load_skill_eval_public_definition(workspace_root: Path, skill_name: str) -> dict[str, Any]:
    return load_split_eval_artifacts(workspace_root, skill_name)["public"]


def load_skill_grading_spec_definition(workspace_root: Path, skill_name: str) -> dict[str, Any]:
    return load_split_eval_artifacts(workspace_root, skill_name)["grading"]


def load_skill_eval_bundle(workspace_root: Path, skill_name: str) -> dict[str, Any]:
    return load_split_eval_artifacts(workspace_root, skill_name)


def snapshot_public_evals(iteration_dir: Path, workspace_root: Path, skill_name: str | None = None) -> dict[str, Any]:
    skill_names = [skill_name] if skill_name else workspace_benchmark_skill_names(workspace_root)
    snapshot: list[dict[str, Any]] = []

    for current_skill in skill_names:
        bundle = load_skill_eval_bundle(workspace_root, current_skill)
        public = bundle["public"]
        snapshot.append(
            {
                "skill_name": current_skill,
                "evals_public_path": bundle["paths"]["public"].relative_to(workspace_root).as_posix(),
                "evals": [
                    {
                        "id": item.get("id"),
                        "prompt": item.get("prompt"),
                        "files": normalize_string_list(item.get("files", [])),
                    }
                    for item in public.get("evals", [])
                    if isinstance(item, dict)
                ],
            }
        )

    payload = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "iteration": iteration_dir.name,
        "skill_count": len(snapshot),
        "skills": snapshot,
    }
    write_json(iteration_dir / "_meta" / "evals-public-snapshot.json", payload)
    return payload


def get_eval_entry(eval_definition: dict[str, Any], eval_id: int) -> dict[str, Any]:
    for item in eval_definition.get("evals", []):
        if item.get("id") == eval_id:
            return item
    raise KeyError(f"No eval with id={eval_id}")


def build_blind_compare_bundle(
    iteration_dir: Path,
    workspace_root: Path,
    skill_name: str,
    eval_id: int,
    run_number: int = 1,
) -> dict[str, Any]:
    eval_dir = iteration_dir / skill_name / f"eval-{eval_id}"
    bundle = load_skill_eval_bundle(workspace_root, skill_name)

    blind_dir = blind_dir_for_run(eval_dir, run_number)
    a_path = blind_dir / "A.md"
    b_path = blind_dir / "B.md"

    if not a_path.exists() or not b_path.exists():
        raise FileNotFoundError(
            f"Missing blind artifacts for {skill_name} eval-{eval_id}: expected {a_path} and {b_path}"
        )

    return {
        "iteration": iteration_dir.name,
        "skill_name": skill_name,
        "eval_id": eval_id,
        "run_number": run_number,
        "blind_artifacts": {
            "A": a_path.relative_to(workspace_root).as_posix(),
            "B": b_path.relative_to(workspace_root).as_posix(),
        },
        "eval_artifacts": {
            "grading_spec_path": bundle["paths"]["grading"].relative_to(workspace_root).as_posix(),
        },
        "comparator_method": {
            "primary_signal": "task-specific rubric score",
            "secondary_signal": "expectation pass rate",
            "tie_policy": "Use TIE only when outputs are genuinely equivalent after rubric and expectation review.",
            "recommended_rubric_dimensions": {
                "content": ["correctness", "completeness", "accuracy"],
                "structure": ["organization", "formatting", "usability"],
            },
        },
        "output_schema_hint": {
            "schema_version": COMPARATOR_SCHEMA_VERSION,
            "eval_id": "integer",
            "run_number": run_number,
            "winner": "A | B | TIE",
            "reasoning": "string",
            "rubric": {
                "A": {
                    "content_score": "0-10 number",
                    "structure_score": "0-10 number",
                    "overall_score": "0-10 number",
                    "notes": "string (optional)",
                },
                "B": {
                    "content_score": "0-10 number",
                    "structure_score": "0-10 number",
                    "overall_score": "0-10 number",
                    "notes": "string (optional)",
                },
            },
            "expectation_results": {
                "A": {"passed": "integer", "total": "integer", "pass_rate": "0-1 number"},
                "B": {"passed": "integer", "total": "integer", "pass_rate": "0-1 number"},
            },
        },
    }


def load_comparison_index(skill_dir: Path) -> dict[tuple[int, int], dict[str, Any]]:
    comparisons_path = skill_dir / "blind-comparisons.json"
    if not comparisons_path.exists():
        return {}
    items = load_comparisons(comparisons_path)
    return {
        (int(item.get("eval_id")), coerce_int(item.get("run_number")) or 1): item
        for item in items
        if item.get("eval_id") is not None
    }


def configuration_side_for_eval(skill_dir: Path, eval_id: int, run_number: int = 1) -> dict[str, str]:
    mapping_path = blind_map_path(skill_dir / f"eval-{eval_id}", run_number)
    if not mapping_path.exists():
        return {}
    mapping = read_json(mapping_path)
    return {config: side for side, config in mapping.items()}


def build_skill_creator_benchmark(iteration_dir: Path, workspace_root: Path, skill_name: str) -> dict[str, Any]:
    skill_dir = iteration_dir / skill_name
    if not skill_dir.exists():
        raise FileNotFoundError(f"Missing skill results directory for '{skill_name}': {skill_dir}")

    eval_bundle = load_skill_eval_bundle(workspace_root, skill_name)
    eval_definition = eval_bundle["grading"]
    comparison_index = load_comparison_index(skill_dir)
    summaries = {
        config: read_json(skill_dir / f"{config}-summary.json")
        for config in ("with_skill", "without_skill")
        if (skill_dir / f"{config}-summary.json").exists()
    }

    runs: list[dict[str, Any]] = []
    notes: list[str] = [
        "Token counts are intentionally omitted in this exported benchmark because the benchmark protocol does not permit inventing token proxies when tokens were not captured.",
        "Per-assertion grading evidence is unavailable in the current benchmark artifacts, so this export preserves aggregate expectation pass rates without fabricating detailed grading rows.",
    ]
    missing_runs: list[str] = []

    for eval_item in eval_definition.get("evals", []):
        eval_id = eval_item.get("id")
        if eval_id is None:
            continue
        expectation_count = len(eval_item.get("expectations", []))

        for configuration in ("with_skill", "without_skill"):
            summary = summaries.get(configuration)
            if not summary:
                missing_runs.append(f"{skill_name} {configuration}: missing summary JSON")
                continue

            summary_runs = summary.get("runs") if isinstance(summary.get("runs"), list) and summary.get("runs") else [
                {
                    "run_number": 1,
                    "summary": summary.get("summary", {}),
                    "evals": summary.get("evals", []),
                }
            ]

            for run_entry in summary_runs:
                run_number = coerce_int(run_entry.get("run_number")) or 1
                eval_row = next((row for row in run_entry.get("evals", []) if row.get("id") == eval_id), None)
                if not eval_row:
                    missing_runs.append(f"{skill_name} eval-{eval_id} {configuration} run-{run_number}: missing response summary row")
                    continue

                response_path = skill_dir / eval_row["response_path"]
                if not response_path.exists():
                    missing_runs.append(f"{skill_name} eval-{eval_id} {configuration} run-{run_number}: missing response file")
                    continue

                comparison_item = comparison_index.get((int(eval_id), run_number))
                side_by_config = configuration_side_for_eval(skill_dir, int(eval_id), run_number)
                pass_rate = None
                if comparison_item and side_by_config.get(configuration):
                    expectation_results = comparison_item.get("expectation_results", {})
                    side = side_by_config[configuration]
                    pass_rate = expectation_results.get(side, {}).get("pass_rate")

                if pass_rate is None:
                    missing_runs.append(f"{skill_name} eval-{eval_id} {configuration} run-{run_number}: missing blind expectation pass rate")
                    continue

                passed = int(round(float(pass_rate) * expectation_count)) if expectation_count else 0
                passed = max(0, min(expectation_count, passed))
                failed = max(0, expectation_count - passed)
                time_seconds = run_entry.get("summary", {}).get("elapsed_seconds_per_eval")

                runs.append(
                    {
                        "eval_id": int(eval_id),
                        "eval_name": f"eval-{eval_id}",
                        "configuration": configuration,
                        "run_number": run_number,
                        "result": {
                            "pass_rate": float(pass_rate),
                            "passed": passed,
                            "failed": failed,
                            "total": expectation_count,
                            "time_seconds": float(time_seconds) if time_seconds is not None else None,
                            "errors": 0,
                        },
                        "expectations": [],
                        "notes": [],
                    }
                )

    if missing_runs:
        notes.append("Missing or incomplete runs were omitted from the exported benchmark:")
        notes.extend(f"- {item}" for item in missing_runs)

    summary_by_config: dict[str, dict[str, Any]] = {}
    for configuration in ("with_skill", "without_skill"):
        config_runs = [run for run in runs if run["configuration"] == configuration]
        pass_rates = [run["result"]["pass_rate"] for run in config_runs if run["result"].get("pass_rate") is not None]
        times = [run["result"]["time_seconds"] for run in config_runs if run["result"].get("time_seconds") is not None]
        summary_by_config[configuration] = {
            "pass_rate": calculate_benchmark_stats(pass_rates),
        }
        if times:
            summary_by_config[configuration]["time_seconds"] = calculate_benchmark_stats(times)

    delta: dict[str, str] = {}
    with_summary = summary_by_config.get("with_skill", {})
    without_summary = summary_by_config.get("without_skill", {})
    if with_summary and without_summary:
        delta_pass = with_summary.get("pass_rate", {}).get("mean", 0.0) - without_summary.get("pass_rate", {}).get("mean", 0.0)
        delta["pass_rate"] = f"{delta_pass:+.2f}"
        with_time = with_summary.get("time_seconds", {}).get("mean")
        without_time = without_summary.get("time_seconds", {}).get("mean")
        if with_time is not None and without_time is not None:
            delta["time_seconds"] = f"{with_time - without_time:+.1f}"
    summary_by_config["delta"] = delta

    included_eval_ids = sorted({run["eval_id"] for run in runs})
    return {
        "metadata": {
            "skill_name": skill_name,
            "skill_path": (workspace_root / ".github" / "skills" / skill_name).relative_to(workspace_root).as_posix(),
            "executor_model": "benchmark-suite-export",
            "analyzer_model": "benchmark-suite-export",
            "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "evals_run": included_eval_ids,
            "runs_per_configuration": max((run.get("run_number", 1) for run in runs), default=1),
        },
        "runs": runs,
        "run_summary": summary_by_config,
        "notes": notes,
    }


def write_skill_creator_benchmark(iteration_dir: Path, workspace_root: Path, skill_name: str, output_path: Path) -> dict[str, Any]:
    benchmark = build_skill_creator_benchmark(iteration_dir, workspace_root, skill_name)
    write_json(output_path, benchmark)
    return benchmark


def locate_workspace_skill_path(workspace_root: Path, skill_name: str) -> Path | None:
    candidate = workspace_root / ".github" / "skills" / skill_name
    if candidate.exists():
        return candidate
    return None


def locate_skill_creator_viewer_script(workspace_root: Path) -> Path:
    skill_creator_root = locate_workspace_skill_path(workspace_root, "skill-creator")
    if not skill_creator_root:
        raise FileNotFoundError("Could not locate the workspace skill 'skill-creator' under .github/skills/")
    script = skill_creator_root / "eval-viewer" / "generate_review.py"
    if not script.exists():
        raise FileNotFoundError(f"Missing skill-creator eval viewer script: {script}")
    return script


def export_review_workspace(iteration_dir: Path, workspace_root: Path, skill_name: str, output_dir: Path) -> dict[str, Any]:
    skill_dir = iteration_dir / skill_name
    if not skill_dir.exists():
        raise FileNotFoundError(f"Missing skill results directory for '{skill_name}': {skill_dir}")

    eval_bundle = load_skill_eval_bundle(workspace_root, skill_name)
    eval_definition = eval_bundle["public"]
    grading_definition = eval_bundle["grading"]

    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    exported_runs: list[dict[str, Any]] = []
    missing_runs: list[dict[str, Any]] = []
    for eval_item in eval_definition.get("evals", []):
        eval_id = eval_item.get("id")
        if eval_id is None:
            continue
        grading_item = get_eval_entry(grading_definition, int(eval_id))
        for configuration in ("with_skill", "without_skill"):
            response_path = resolve_response_path(skill_dir, int(eval_id), configuration, 1)
            if response_path is None:
                missing_runs.append(
                    {
                        "eval_id": eval_id,
                        "configuration": configuration,
                        "expected_path": legacy_response_path(skill_dir, int(eval_id), configuration).relative_to(workspace_root).as_posix(),
                    }
                )
                continue

            run_dir = output_dir / f"eval-{eval_id}" / configuration
            outputs_dir = run_dir / "outputs"
            outputs_dir.mkdir(parents=True, exist_ok=True)
            write_text(outputs_dir / "response.md", response_path.read_text(encoding="utf-8"))
            write_json(
                run_dir / "eval_metadata.json",
                {
                    "eval_id": eval_id,
                    "eval_name": f"eval-{eval_id}-{configuration}",
                    "skill_name": skill_name,
                    "configuration": configuration,
                    "prompt": eval_item.get("prompt", ""),
                    "expected_output": grading_item.get("expected_output", ""),
                    "assertions": grading_item.get("expectations", []),
                },
            )
            exported_runs.append(
                {
                    "eval_id": eval_id,
                    "configuration": configuration,
                    "run_dir": run_dir.relative_to(workspace_root).as_posix(),
                }
            )

    summary = {
        "iteration": iteration_dir.name,
        "skill_name": skill_name,
        "output_dir": output_dir.relative_to(workspace_root).as_posix(),
        "expected_run_count": len(eval_definition.get("evals", [])) * 2,
        "run_count": len(exported_runs),
        "missing_run_count": len(missing_runs),
        "missing_runs": missing_runs,
        "runs": exported_runs,
    }
    return summary


def build_grader_bundle(
    iteration_dir: Path,
    workspace_root: Path,
    skill_name: str,
    eval_id: int,
    configuration: str,
    export_dir: Path | None = None,
) -> dict[str, Any]:
    output_dir = export_dir or (iteration_dir / skill_name / "_skill-creator-review-workspace")
    export_review_workspace(iteration_dir, workspace_root, skill_name, output_dir)

    eval_bundle = load_skill_eval_bundle(workspace_root, skill_name)
    public_entry = get_eval_entry(eval_bundle["public"], eval_id)
    grading_entry = get_eval_entry(eval_bundle["grading"], eval_id)
    run_dir = output_dir / f"eval-{eval_id}" / configuration
    outputs_dir = run_dir / "outputs"
    if not outputs_dir.exists():
        raise FileNotFoundError(f"Missing exported outputs directory for {skill_name} eval-{eval_id} {configuration}: {outputs_dir}")

    transcript_path = None
    for candidate in (run_dir / "transcript.md", outputs_dir / "transcript.md"):
        if candidate.exists():
            transcript_path = candidate.relative_to(workspace_root).as_posix()
            break

    notes = []
    if transcript_path is None:
        notes.append(
            "No execution transcript is available in the current benchmark export, so the grader can only verify output-facing expectations rather than process-following assertions."
        )

    return {
        "iteration": iteration_dir.name,
        "skill_name": skill_name,
        "eval_id": eval_id,
        "configuration": configuration,
        "grader_playbook": "skill-creator/agents/grader.md",
        "prompt": public_entry.get("prompt"),
        "expected_output": grading_entry.get("expected_output"),
        "expectations": grading_entry.get("expectations", []),
        "eval_artifacts": {
            "evals_public_path": eval_bundle["paths"]["public"].relative_to(workspace_root).as_posix(),
            "grading_spec_path": eval_bundle["paths"]["grading"].relative_to(workspace_root).as_posix(),
        },
        "inputs": {
            "outputs_dir": outputs_dir.relative_to(workspace_root).as_posix(),
            "transcript_path": transcript_path,
        },
        "output_path": (run_dir / "grading.json").relative_to(workspace_root).as_posix(),
        "notes": notes,
    }


def build_benchmark_analysis_bundle(iteration_dir: Path, workspace_root: Path, skill_name: str) -> dict[str, Any]:
    skill_dir = iteration_dir / skill_name
    if not skill_dir.exists():
        raise FileNotFoundError(f"Missing skill results directory for '{skill_name}': {skill_dir}")

    eval_bundle = load_skill_eval_bundle(workspace_root, skill_name)

    previous_iteration = find_previous_iteration(iteration_dir.parent, iteration_dir)
    previous_paths = None
    if previous_iteration and (previous_iteration / skill_name).exists():
        previous_paths = {
            "iteration": previous_iteration.name,
            "skill_dir": (previous_iteration / skill_name).relative_to(workspace_root).as_posix(),
            "suite_summary": (previous_iteration / "suite-summary.json").relative_to(workspace_root).as_posix()
            if (previous_iteration / "suite-summary.json").exists()
            else None,
        }

    return {
        "iteration": iteration_dir.name,
        "skill_name": skill_name,
        "analyzer_playbook": "skill-creator/agents/analyzer.md",
        "inputs": {
            "skill_dir": skill_dir.relative_to(workspace_root).as_posix(),
            "evals_public_path": eval_bundle["paths"]["public"].relative_to(workspace_root).as_posix(),
            "grading_spec_path": eval_bundle["paths"]["grading"].relative_to(workspace_root).as_posix(),
            "blind_comparisons_path": (skill_dir / "blind-comparisons.json").relative_to(workspace_root).as_posix(),
            "with_skill_summary_path": (skill_dir / "with_skill-summary.json").relative_to(workspace_root).as_posix(),
            "without_skill_summary_path": (skill_dir / "without_skill-summary.json").relative_to(workspace_root).as_posix(),
            "suite_summary_path": (iteration_dir / "suite-summary.json").relative_to(workspace_root).as_posix()
            if (iteration_dir / "suite-summary.json").exists()
            else None,
        },
        "previous_iteration": previous_paths,
        "analysis_focus": [
            "Which expectations are non-discriminating, flaky, or too easy?",
            "Where does the skill improve quality versus only adding verbosity?",
            "Which evals end in ties despite different practical usefulness?",
            "Which blind wins or losses should drive the next skill revision?",
        ],
    }


# ---------------------------------------------------------------------------
# Synthesis bundle & writer
# ---------------------------------------------------------------------------


def build_synthesis_bundle(
    iteration_dir: Path,
    workspace_root: Path,
    skill_name: str,
) -> dict[str, Any]:
    """Build a comprehensive data bundle for generating a critical synthesis report.

    The bundle includes all quantitative metrics, per-eval blind comparison
    details, executable validity data, and eval definitions.  An LLM agent
    reads this bundle to produce the synthesis markdown.
    """
    skill_dir = iteration_dir / skill_name
    if not skill_dir.exists():
        raise FileNotFoundError(f"Missing skill results directory for '{skill_name}': {skill_dir}")

    # -- eval definitions --
    eval_bundle = load_skill_eval_bundle(workspace_root, skill_name)
    public_evals = eval_bundle["public"].get("evals", [])
    grading_evals = {int(e["id"]): e for e in eval_bundle["grading"].get("evals", []) if e.get("id") is not None}

    # -- summaries --
    with_summary = read_json(skill_dir / "with_skill-summary.json") if (skill_dir / "with_skill-summary.json").exists() else {}
    without_summary = read_json(skill_dir / "without_skill-summary.json") if (skill_dir / "without_skill-summary.json").exists() else {}
    with_metrics = load_summary_metrics(skill_dir / "with_skill-summary.json") if (skill_dir / "with_skill-summary.json").exists() else {}
    without_metrics = load_summary_metrics(skill_dir / "without_skill-summary.json") if (skill_dir / "without_skill-summary.json").exists() else {}

    # -- blind comparisons --
    comparisons_path = skill_dir / "blind-comparisons.json"
    comparison_items = load_comparisons(comparisons_path) if comparisons_path.exists() else []

    # Build per-eval mapping: eval_id -> {winner_config, reasoning, rubric, expectations}
    per_eval_comparisons: list[dict[str, Any]] = []
    for item in comparison_items:
        eval_id = item.get("eval_id")
        if eval_id is None:
            continue
        eval_id = int(eval_id)
        run_number = coerce_int(item.get("run_number")) or 1
        mapping_path = blind_map_path(skill_dir / f"eval-{eval_id}", run_number)
        mapping = read_json(mapping_path) if mapping_path.exists() else {}
        reverse_mapping = {config: side for side, config in mapping.items()}

        winner_raw = item.get("winner")
        winner_config = mapping.get(winner_raw, "TIE") if winner_raw != "TIE" else "TIE"

        rubric = item.get("rubric", {})
        with_side = reverse_mapping.get("with_skill")
        without_side = reverse_mapping.get("without_skill")
        with_rubric = rubric.get(with_side, {}).get("overall_score") if with_side else None
        without_rubric = rubric.get(without_side, {}).get("overall_score") if without_side else None
        with_notes = rubric.get(with_side, {}).get("notes", "") if with_side else ""
        without_notes = rubric.get(without_side, {}).get("notes", "") if without_side else ""

        exp_results = item.get("expectation_results", {})
        with_exp = exp_results.get(with_side, {}) if with_side else {}
        without_exp = exp_results.get(without_side, {}) if without_side else {}

        # Determine confidence from rubric delta
        rubric_delta = (with_rubric - without_rubric) if with_rubric is not None and without_rubric is not None else 0
        confidence = "high" if abs(rubric_delta) >= 3 else "medium" if abs(rubric_delta) >= 1 else "low"

        # Grab eval prompt & expected output for context
        eval_prompt = ""
        expected_output = ""
        grading_entry = grading_evals.get(eval_id, {})
        for pub in public_evals:
            if int(pub.get("id", -1)) == eval_id:
                eval_prompt = pub.get("prompt", "")
                break
        expected_output = grading_entry.get("expected_output", "")
        expectations = grading_entry.get("expectations", [])

        per_eval_comparisons.append({
            "eval_id": eval_id,
            "run_number": run_number,
            "eval_prompt": eval_prompt,
            "expected_output": expected_output,
            "expectations": expectations,
            "winner": winner_config,
            "confidence": confidence,
            "reasoning": item.get("reasoning", ""),
            "with_skill_rubric_score": with_rubric,
            "without_skill_rubric_score": without_rubric,
            "with_skill_rubric_notes": with_notes,
            "without_skill_rubric_notes": without_notes,
            "with_skill_expectations": {
                "passed": with_exp.get("passed", 0),
                "total": with_exp.get("total", 0),
            },
            "without_skill_expectations": {
                "passed": without_exp.get("passed", 0),
                "total": without_exp.get("total", 0),
            },
        })

    per_eval_comparisons.sort(key=lambda x: (x["eval_id"], x["run_number"]))

    # -- executable validity --
    with_executable = load_executable_check_metrics(skill_dir / "with_skill-executable-checks.json")
    without_executable = load_executable_check_metrics(skill_dir / "without_skill-executable-checks.json")

    # -- suite-level data --
    suite_summary_path = iteration_dir / "suite-summary.json"
    suite_summary = read_json(suite_summary_path) if suite_summary_path.exists() else {}

    # -- quantitative overview --
    with_s = with_summary.get("summary", {})
    without_s = without_summary.get("summary", {})
    cap = comparison_metrics(skill_dir, comparison_items)
    eval_count = len(public_evals)
    run_count = max(with_metrics.get("run_count", 1), without_metrics.get("run_count", 1))

    # -- protocol metadata --
    protocol_lock_path = iteration_dir / "_meta" / "protocol-lock.json"
    protocol_lock = read_json(protocol_lock_path) if protocol_lock_path.exists() else {}

    return {
        "iteration": iteration_dir.name,
        "skill_name": skill_name,
        "protocol_version": protocol_lock.get("protocol_version"),
        "generated_at": utc_now_iso(),
        "eval_count": eval_count,
        "run_count": run_count,
        "quantitative": {
            "blind": {
                "with_skill_wins": cap["blind"]["with_skill_wins"],
                "without_skill_wins": cap["blind"]["without_skill_wins"],
                "ties": cap["blind"]["ties"],
                "with_skill_win_rate": cap["blind"]["with_skill_win_rate"],
            },
            "expectation_pass_rate": {
                "with_skill": cap["expectation_pass_rate"]["with_skill"],
                "without_skill": cap["expectation_pass_rate"]["without_skill"],
                "delta": cap["expectation_pass_rate"]["delta"],
            },
            "rubric_score": {
                "with_skill": cap["rubric_score"]["with_skill"],
                "without_skill": cap["rubric_score"]["without_skill"],
                "delta": cap["rubric_score"]["delta"],
            },
            "time_per_eval": {
                "with_skill": with_s.get("elapsed_seconds_per_eval"),
                "without_skill": without_s.get("elapsed_seconds_per_eval"),
                "delta": delta_or_none(with_s.get("elapsed_seconds_per_eval"), without_s.get("elapsed_seconds_per_eval")),
            },
            "words_per_eval": {
                "with_skill": with_s.get("response_words_per_eval"),
                "without_skill": without_s.get("response_words_per_eval"),
                "delta": delta_or_none(with_s.get("response_words_per_eval"), without_s.get("response_words_per_eval")),
            },
            "files_read": {
                "with_skill": with_s.get("files_read_count"),
                "without_skill": without_s.get("files_read_count"),
                "delta": delta_or_none(with_s.get("files_read_count"), without_s.get("files_read_count")),
            },
            "executable_validity": {
                "with_skill": with_executable.get("valid_eval_rate") if with_executable else None,
                "without_skill": without_executable.get("valid_eval_rate") if without_executable else None,
                "delta": delta_or_none(
                    with_executable.get("valid_eval_rate") if with_executable else None,
                    without_executable.get("valid_eval_rate") if without_executable else None,
                ),
            },
        },
        "per_eval_comparisons": per_eval_comparisons,
        "executable_details": {
            "with_skill": with_executable,
            "without_skill": without_executable,
        },
        "high_variance_evals": cap.get("high_variance_evals", []),
        "synthesis_template": SYNTHESIS_TEMPLATE,
    }


SYNTHESIS_TEMPLATE = """# Critical Synthesis — `{skill_name}` Benchmark

**Iteration:** `{iteration}`
**Protocol:** {protocol_version}
**Evals:** {eval_count} (ids {eval_id_range}), {run_count} run(s) per configuration
**Generated:** {date}

---

## 1. Quantitative results

| Metric | `with_skill` | `without_skill` | Δ |
|---|---|---|---|
| **Blind win rate** | **{with_wins}/{total_comparisons} = {with_win_pct}** | {without_wins}/{total_comparisons} = {without_win_pct} | {win_rate_delta} |
| **Expectation pass rate** | **{with_exp_rate}** | {without_exp_rate} | **{exp_delta}** |
| **Rubric score (0–10)** | **{with_rubric}** | {without_rubric} | **{rubric_delta}** |
| Seconds / eval | {with_time} s | {without_time} s | {time_delta} |
| Words / eval | {with_words} | {without_words} | {words_delta} |
| Files read | {with_files} | {without_files} | {files_delta} |
| Executable validity | {with_exec} | {without_exec} | {exec_delta} |

[Interpret the quantitative results: what is the overall signal? Is it strong, weak, mixed?]

---

## 2. Eval-by-eval analysis

| Eval | Topic | Winner | Exp with | Exp without | Key discriminator |
|---|---|---|---|---|---|
[One row per eval — fill in from per_eval_comparisons data]

### Observations

[For each notable eval, explain WHY the winner won. Use the blind comparison reasoning and rubric notes. Identify the strongest signals and the weakest discriminators.]

---

## 3. Executable validity analysis

[Analyze the executable validity delta. If skill scores lower despite winning blind comparisons, explain the paradox (e.g. shell commands vs DSL blocks). State whether this metric is reliable for this skill.]

---

## 4. Skill design assessment

### Strengths
[Based on eval-by-eval wins: what does the skill teach that the baseline cannot infer? List 3-4 concrete strengths.]

### Weak areas
[Based on narrow wins, ties, or low-confidence comparisons: where could the skill improve? List 3-4 areas with specific eval references.]

---

## 5. Priority recommendations

**P1 — Critical (direct impact on baseline failures)**
[Actions that would fix the largest baseline gaps]

**P2 — Important (improved precision)**
[Actions that would strengthen narrow wins]

**P3 — Nice to have (robustness)**
[Follow-up experiments or eval additions]

---

## 6. Anthropic skill-authoring best-practices pass

- **Concision / token economy:** [Identify instructions to trim because they restate model-common knowledge instead of adding task-critical guidance]
- **Degrees of freedom fit:** [Assess where guidance should be looser (context-driven) vs stricter (fragile sequences) and why]
- **Triggerability metadata quality:** [Assess whether `name` + `description` clearly communicate capability and trigger contexts]
- **Progressive disclosure quality:** [Check whether SKILL.md stays focused and references remain one level deep to detailed files]
- **Workflow + feedback-loop quality:** [Confirm complex tasks include a clear sequence and a validate/fix/retry loop]
- **Anti-pattern scan + rewrites:** [Flag vague wording, option overload, stale/time-sensitive guidance, or path/platform pitfalls; propose concrete rewrite edits]

---

## 7. Verdict

[State whether the skill is effective, with a 2-3 sentence summary citing the key metrics. Note any caveats.]
"""


def render_synthesis_quantitative_section(bundle: dict[str, Any]) -> str:
    """Pre-render the quantitative table from a synthesis bundle."""
    q = bundle["quantitative"]

    def fmt(v: Any, decimals: int = 3, suffix: str = "") -> str:
        if v is None:
            return "—"
        return f"{round(float(v), decimals)}{suffix}"

    def fmt_pct(v: Any) -> str:
        if v is None:
            return "—"
        return f"{round(float(v) * 100, 1)}%"

    def fmt_delta(v: Any, decimals: int = 3) -> str:
        if v is None:
            return "—"
        val = round(float(v), decimals)
        return f"+{val}" if val > 0 else str(val)

    blind = q["blind"]
    total = blind["with_skill_wins"] + blind.get("without_skill_wins", 0) + blind.get("ties", 0)

    lines = [
        f"| **Blind win rate** | **{blind['with_skill_wins']}/{total} = {fmt_pct(blind['with_skill_win_rate'])}** | {blind.get('without_skill_wins', 0)}/{total} = {fmt_pct(1.0 - float(blind['with_skill_win_rate']) if blind['with_skill_win_rate'] is not None else None)} | {fmt_delta(float(blind['with_skill_win_rate'] or 0) - (1.0 - float(blind['with_skill_win_rate'] or 0)))} |",
        f"| **Expectation pass rate** | **{fmt(q['expectation_pass_rate']['with_skill'])} ({fmt_pct(q['expectation_pass_rate']['with_skill'])})** | {fmt(q['expectation_pass_rate']['without_skill'])} ({fmt_pct(q['expectation_pass_rate']['without_skill'])}) | **{fmt_delta(q['expectation_pass_rate']['delta'])}** |",
        f"| **Rubric score (0–10)** | **{fmt(q['rubric_score']['with_skill'])}** | {fmt(q['rubric_score']['without_skill'])} | **{fmt_delta(q['rubric_score']['delta'])}** |",
        f"| Seconds / eval | {fmt(q['time_per_eval']['with_skill'], 1)} s | {fmt(q['time_per_eval']['without_skill'], 1)} s | {fmt_delta(q['time_per_eval']['delta'], 1)} s |",
        f"| Words / eval | {fmt(q['words_per_eval']['with_skill'], 1)} | {fmt(q['words_per_eval']['without_skill'], 1)} | {fmt_delta(q['words_per_eval']['delta'], 1)} |",
        f"| Files read | {fmt(q['files_read']['with_skill'], 1)} | {fmt(q['files_read']['without_skill'], 1)} | {fmt_delta(q['files_read']['delta'], 1)} |",
        f"| Executable validity | {fmt(q['executable_validity']['with_skill'])} | {fmt(q['executable_validity']['without_skill'])} | {fmt_delta(q['executable_validity']['delta'])} |",
    ]
    return "\n".join(lines)


def render_synthesis_eval_table(bundle: dict[str, Any]) -> str:
    """Pre-render the eval-by-eval comparison table from a synthesis bundle."""
    rows: list[str] = []
    for comp in bundle["per_eval_comparisons"]:
        winner = comp["winner"]
        confidence = comp["confidence"]
        with_p = comp["with_skill_expectations"]["passed"]
        with_t = comp["with_skill_expectations"]["total"]
        without_p = comp["without_skill_expectations"]["passed"]
        without_t = comp["without_skill_expectations"]["total"]
        rows.append(
            f"| **{comp['eval_id']}** | [topic] | {winner} ({confidence}) | {with_p}/{with_t} | {without_p}/{without_t} | [key discriminator] |"
        )
    return "\n".join(rows)


def cmd_synthesis_bundle(args: argparse.Namespace) -> None:
    bundle = build_synthesis_bundle(args.iteration, args.workspace_root, args.skill)
    print(json.dumps(bundle, indent=2, ensure_ascii=False))


def cmd_write_synthesis(args: argparse.Namespace) -> None:
    skill_dir = args.iteration / args.skill
    if not skill_dir.exists():
        raise FileNotFoundError(f"Missing skill results directory for '{args.skill}': {skill_dir}")
    if args.content_file:
        content = args.content_file.resolve().read_text(encoding="utf-8")
    else:
        content = sys.stdin.read()
    output_path = (args.output.resolve() if args.output else None) or (skill_dir / "synthesis.md")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    write_text(output_path, content)
    print(json.dumps({
        "iteration": args.iteration.name,
        "skill_name": args.skill,
        "output_path": output_path.relative_to(args.workspace_root).as_posix(),
        "content_length": len(content),
    }, indent=2, ensure_ascii=False))


def write_static_review(iteration_dir: Path, workspace_root: Path, skill_name: str, output_html: Path) -> dict[str, Any]:
    current_workspace = iteration_dir / skill_name / "_skill-creator-review-workspace"
    current_export = export_review_workspace(iteration_dir, workspace_root, skill_name, current_workspace)
    benchmark_path = iteration_dir / skill_name / "skill-creator-benchmark.json"
    benchmark = write_skill_creator_benchmark(iteration_dir, workspace_root, skill_name, benchmark_path)

    previous_iteration = find_previous_iteration(iteration_dir.parent, iteration_dir)
    previous_workspace = None
    previous_export = None
    if previous_iteration and (previous_iteration / skill_name).exists():
        previous_workspace = iteration_dir / skill_name / f"_skill-creator-review-workspace-{previous_iteration.name}"
        previous_export = export_review_workspace(previous_iteration, workspace_root, skill_name, previous_workspace)

    viewer_script = locate_skill_creator_viewer_script(workspace_root)
    command = [
        sys.executable,
        str(viewer_script),
        str(current_workspace),
        "--skill-name",
        skill_name,
        "--benchmark",
        str(benchmark_path),
        "--static",
        str(output_html),
    ]
    if previous_workspace is not None:
        command.extend(["--previous-workspace", str(previous_workspace)])

    result = subprocess.run(command, capture_output=True, text=True, check=False, cwd=workspace_root)
    if result.returncode != 0:
        raise RuntimeError(
            f"skill-creator eval viewer failed with exit code {result.returncode}: {result.stderr or result.stdout}"
        )

    return {
        "iteration": iteration_dir.name,
        "skill_name": skill_name,
        "output_html": output_html.relative_to(workspace_root).as_posix(),
        "benchmark_json": benchmark_path.relative_to(workspace_root).as_posix(),
        "benchmark_run_count": len(benchmark.get("runs", [])),
        "current_workspace": current_export["output_dir"],
        "previous_workspace": previous_export["output_dir"] if previous_export else None,
        "viewer_script": str(viewer_script),
        "viewer_stdout": result.stdout.strip(),
    }


def selected_baseline_agent(baseline_isolation: str) -> str:
    if baseline_isolation == "hook-only":
        return BENCHMARK_AGENTS["without_skill_hook_only"]
    return BENCHMARK_AGENTS["without_skill"]


def benchmark_agent_plan(
    iteration_dir: Path,
    skill: str | None = None,
    baseline_isolation: str = "relocation",
) -> dict[str, Any]:
    baseline_agent = selected_baseline_agent(baseline_isolation)
    notes = [
        "Enable chat.useCustomAgentHooks = true before using the benchmark agents.",
        f"Human entrypoint: use the workspace custom agent '{INTERACTIVE_ENTRYPOINT}'.",
        f"Automation entrypoint: use '{AUTOMATION_ENTRYPOINT}' for offline checks.",
        "The benchmark manager may delegate only to the constrained benchmark worker agents.",
        "Benchmark worker agents are read-only and set agents: [] so they cannot chain into unconstrained subagents.",
        "Only narrow LikeC4 MCP grounding is allowed in baseline, hook-only baseline, and with-skill workers; project listing, project summaries, and view browsing stay blocked, and benchmark_manager/blind_compare keep MCP disabled.",
    ]
    if baseline_isolation == "hook-only":
        notes.append(
            "Hook-only baseline isolation is an explicit experiment mode. Keep it separate from the strict relocated baseline until repeated runs prove it is trustworthy."
        )
    else:
        notes.append(
            "Keep the physical relocation step for the strict without_skill phase; hooks strengthen isolation but do not replace it."
        )
    if skill:
        notes.append(
            f"For with_skill runs, open a fresh session with {BENCHMARK_AGENTS['with_skill']} and read only the target skill '{skill}'."
        )
    else:
        notes.append(
            "When a campaign covers only part of the skill space, build each phase matrix from that selected subset only; do not serialize across untouched skills."
        )
    notes.append(
        "Default execution mode is parallel within each phase: launch independent worker sessions concurrently, then wait for all of them to finish before advancing the phase."
    )
    notes.append(
        "If resolved hook audit entries show missing raw sessionId values, ensure workers still receive disjoint derived anonymous sessions (per skill / blind scope). If a run is interrupted or reused, clear stale anonymous hook state between fresh workers with `python test/scripts/skill_suite_tools.py reset-hook-state --workspace-root . --mode <mode>`."
    )
    notes.append(
        "Never overlap without_skill and with_skill phases; keep phase boundaries sequential even when workers inside a phase run in parallel."
    )

    return {
        "iteration": iteration_dir.name,
        "protocol_version": BENCHMARK_PROTOCOL_VERSION,
        "required_setting": {
            "chat.useCustomAgentHooks": True,
        },
        "agents": BENCHMARK_AGENTS,
        "baseline_isolation": baseline_isolation,
        "parallelism": {
            "default_policy": "parallel-within-phase",
            "cross_phase_parallelism": "forbidden",
            "unit_of_parallelism": "<skill, eval_id, configuration, run_number>",
            "phase_barrier": "wait for all tasks in the current phase before starting the next one",
            "safe_parallel_condition": "parallelize only tasks whose output directories do not overlap",
            "anonymous_stateful_fallback": "derive per-scope anonymous sessions; if scope derivation cannot be maintained, reset-hook-state and serialize as a safety fallback",
            "fallback_policy": "if runtime or platform limits are hit, reduce concurrency before falling back to serial execution",
        },
        "entrypoints": {
            "interactive": INTERACTIVE_ENTRYPOINT,
            "automation": AUTOMATION_ENTRYPOINT,
            "preflight": f"python test/scripts/skill_suite_tools.py protocol-preflight --iteration {iteration_dir.as_posix()} --workspace-root .",
        },
        "phases": [
            {
                "phase": "without_skill",
                "agent": baseline_agent,
                "dispatch_mode": "parallel",
                "parallel_scope": "<skill, eval_id, run_number>",
                "precondition": (
                    "Workspace skills were physically moved out of .github/skills/ and fresh workers were started afterwards."
                    if baseline_isolation != "hook-only"
                    else "Workspace skills may remain in place, but the baseline run is an explicit hook-only isolation probe."
                ),
            },
            {
                "phase": "with_skill",
                "agent": BENCHMARK_AGENTS["with_skill"],
                "dispatch_mode": "parallel",
                "parallel_scope": "<skill, eval_id, run_number>",
                "precondition": "Workspace skills were restored and each fresh worker stays inside one target skill directory.",
                "anonymous_session_fallback": "derived anonymous sessions per skill; if unresolved, serial with reset-hook-state --mode with_skill_targeted",
                "target_skill": skill,
            },
            {
                "phase": "blind_compare",
                "agent": BENCHMARK_AGENTS["blind_compare"],
                "dispatch_mode": "parallel",
                "parallel_scope": "<skill, eval_id, run_number>",
                "precondition": "Only blind A/B artifacts and the target eval definitions are exposed to the comparator.",
                "anonymous_session_fallback": "derived anonymous sessions per blind scope; if unresolved, serial with reset-hook-state --mode blind_compare",
            },
        ],
        "notes": notes,
    }


def validate_blind_isolation(iteration_dir: Path) -> dict[str, Any]:
    issues: list[dict[str, Any]] = []
    checked_skills = 0
    checked_evals = 0

    for skill_dir in skill_dirs(iteration_dir):
        checked_skills += 1
        comparisons_path = skill_dir / "blind-comparisons.json"
        if comparisons_path.exists():
            comparisons_text = comparisons_path.read_text(encoding="utf-8")
            for forbidden in BLIND_FORBIDDEN_TOKENS:
                if forbidden in comparisons_text:
                    issues.append(
                        {
                            "skill": skill_dir.name,
                            "path": comparisons_path.relative_to(iteration_dir).as_posix(),
                            "issue": f"forbidden token '{forbidden}' leaked into blind-comparisons.json",
                        }
                    )

        for eval_dir in sorted(skill_dir.glob("eval-*"), key=lambda path: path.name):
            blind_root = eval_dir / "blind"
            if not blind_root.exists():
                continue
            checked_evals += 1

            run_dirs: list[Path] = sorted(
                sorted(
                    [child for child in blind_root.iterdir() if child.is_dir() and RUN_DIR_RE.match(child.name)],
                    key=lambda path: int(path.name.split("-", 1)[1]),
                )
            )

            legacy_files = sorted(
                child.name
                for child in blind_root.iterdir()
                if child.is_file() and child.name in {"A.md", "B.md", "blind-map.json"}
            )
            if legacy_files:
                issues.append(
                    {
                        "skill": skill_dir.name,
                        "path": blind_root.relative_to(iteration_dir).as_posix(),
                        "issue": f"legacy blind files are no longer allowed at blind root: {', '.join(legacy_files)}",
                    }
                )

            if not run_dirs:
                issues.append(
                    {
                        "skill": skill_dir.name,
                        "path": blind_root.relative_to(iteration_dir).as_posix(),
                        "issue": "missing run-* blind directory",
                    }
                )
                continue

            for run_dir in run_dirs:
                if run_dir.parent != blind_root:
                    continue

                run_number = 1
                if run_dir != blind_root:
                    run_number = int(run_dir.name.split("-", 1)[1])

                for required_name in ("A.md", "B.md"):
                    if not (run_dir / required_name).exists():
                        issues.append(
                            {
                                "skill": skill_dir.name,
                                "path": run_dir.relative_to(iteration_dir).as_posix(),
                                "issue": f"missing {required_name}",
                            }
                        )

                extra_files = sorted(
                    child.name
                    for child in run_dir.iterdir()
                    if child.is_file() and child.name not in {"A.md", "B.md"}
                )
                if extra_files:
                    issues.append(
                        {
                            "skill": skill_dir.name,
                            "path": run_dir.relative_to(iteration_dir).as_posix(),
                            "issue": f"unexpected files in blind directory: {', '.join(extra_files)}",
                        }
                    )

                if (run_dir / "blind-map.json").exists():
                    issues.append(
                        {
                            "skill": skill_dir.name,
                            "path": run_dir.relative_to(iteration_dir).as_posix(),
                            "issue": "blind-map.json must stay outside the blind/ directory",
                        }
                    )

                expected_map_path = blind_map_path(eval_dir, run_number)
                if not expected_map_path.exists():
                    issues.append(
                        {
                            "skill": skill_dir.name,
                            "path": eval_dir.relative_to(iteration_dir).as_posix(),
                            "issue": f"missing {expected_map_path.name} beside the eval directory",
                        }
                    )

    return {
        "iteration": iteration_dir.name,
        "checked_skills": checked_skills,
        "checked_evals": checked_evals,
        "issue_count": len(issues),
        "issues": issues,
        "passed": len(issues) == 0,
    }


def run_command(command: list[str], workspace_root: Path) -> dict[str, Any]:
    result = subprocess.run(command, capture_output=True, text=True, check=False, cwd=workspace_root)
    return {
        "command": " ".join(command),
        "returncode": result.returncode,
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip(),
        "passed": result.returncode == 0,
    }


def preview_jsonl_line(raw_line: str, limit: int = 200) -> str:
    preview = raw_line.strip().replace("\t", "\\t")
    if len(preview) <= limit:
        return preview
    return preview[: max(1, limit - 1)] + "…"


def load_jsonl_records_with_issues(path: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    if not path.exists():
        raise FileNotFoundError(f"Missing JSONL file: {path}")

    entries: list[dict[str, Any]] = []
    issues: list[dict[str, Any]] = []
    for line_number, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw_line.strip()
        if not line:
            continue
        try:
            payload = json.loads(line)
        except json.JSONDecodeError as exc:
            issues.append(
                {
                    "line_number": line_number,
                    "problem": "malformed-jsonl-line",
                    "reason": str(exc),
                    "raw_preview": preview_jsonl_line(raw_line),
                }
            )
            continue
        if not isinstance(payload, dict):
            issues.append(
                {
                    "line_number": line_number,
                    "problem": "non-object-jsonl-line",
                    "reason": f"JSONL entry must be an object, got {type(payload).__name__}",
                    "raw_preview": preview_jsonl_line(raw_line),
                }
            )
            continue
        payload["_line_number"] = line_number
        entries.append(payload)
    return entries, issues


def load_jsonl_records(path: Path) -> list[dict[str, Any]]:
    entries, issues = load_jsonl_records_with_issues(path)
    if issues:
        first_issue = issues[0]
        raise ValueError(
            f"Invalid JSONL entry at line {first_issue['line_number']} ({first_issue['problem']}): {path}"
        )
    return entries


def normalize_hook_tool_name(tool_name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", tool_name.lower())


def is_hook_audit_read_allowed(rel_path: str, mode: str) -> bool:
    prefixes = HOOK_AUDIT_ALLOWED_READ_PREFIXES.get(mode, ())
    if rel_path.startswith("@external/"):
        return False
    return any(rel_path.startswith(prefix) for prefix in prefixes)


def validate_hook_audit(path: Path, mode: str | None = None) -> dict[str, Any]:
    entries, parse_issues = load_jsonl_records_with_issues(path)
    issues: list[dict[str, Any]] = [
        {
            "line_number": issue["line_number"],
            "mode": None,
            "tool_name": None,
            "problem": issue["problem"],
            "reason": issue["reason"],
            "raw_preview": issue["raw_preview"],
        }
        for issue in parse_issues
    ]
    filtered_entries: list[dict[str, Any]] = []

    for entry in entries:
        entry_mode = entry.get("mode")
        if mode and entry_mode != mode:
            continue
        filtered_entries.append(entry)

        if entry.get("permissionDecision") != "allow":
            continue

        tool_name = str(entry.get("tool_name", ""))
        normalized_tool = normalize_hook_tool_name(tool_name)
        tool_paths = [value for value in entry.get("tool_paths", []) if isinstance(value, str)]

        if entry_mode in {"baseline", "baseline_hook_only", "with_skill_targeted"}:
            if normalized_tool in RESTRICTED_LIKEC4_MCP_NORMALIZED_NAMES:
                issues.append(
                    {
                        "line_number": entry.get("_line_number"),
                        "mode": entry_mode,
                        "tool_name": tool_name,
                        "problem": "allowed-broad-likec4-mcp",
                        "reason": entry.get("permissionDecisionReason"),
                    }
                )

            if tool_name.startswith("mcp_") and not tool_name.startswith("mcp_likec4_"):
                issues.append(
                    {
                        "line_number": entry.get("_line_number"),
                        "mode": entry_mode,
                        "tool_name": tool_name,
                        "problem": "allowed-non-likec4-mcp",
                        "reason": entry.get("permissionDecisionReason"),
                    }
                )

            if tool_name == "read_file":
                for rel_path in tool_paths:
                    if is_hook_audit_read_allowed(rel_path, entry_mode):
                        continue
                    issues.append(
                        {
                            "line_number": entry.get("_line_number"),
                            "mode": entry_mode,
                            "tool_name": tool_name,
                            "path": rel_path,
                            "problem": "allowed-read-outside-mode-scope",
                            "reason": entry.get("permissionDecisionReason"),
                        }
                    )

        if entry_mode == "blind_compare" and tool_name.startswith("mcp_"):
            issues.append(
                {
                    "line_number": entry.get("_line_number"),
                    "mode": entry_mode,
                    "tool_name": tool_name,
                    "problem": "allowed-mcp-in-blind-compare",
                    "reason": entry.get("permissionDecisionReason"),
                }
            )

    timestamps = [entry.get("timestamp") for entry in filtered_entries if isinstance(entry.get("timestamp"), str) and entry.get("timestamp", "").strip()]
    return {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "path": path.as_posix(),
        "mode": mode,
        "entry_count": len(filtered_entries),
        "malformed_line_count": len(parse_issues),
        "first_timestamp": timestamps[0] if timestamps else None,
        "last_timestamp": timestamps[-1] if timestamps else None,
        "issue_count": len(issues),
        "issues": issues,
        "passed": len(issues) == 0,
    }


def run_self_test(iteration_dir: Path, workspace_root: Path, baseline_isolation: str) -> dict[str, Any]:
    policy_test = run_command([sys.executable, "test/scripts/tests/test_benchmark_agent_policy.py"], workspace_root)
    harness_test = run_command([sys.executable, "test/scripts/tests/test_skill_suite_tools.py"], workspace_root)
    blind_isolation = validate_blind_isolation(iteration_dir)
    viewer_script = locate_skill_creator_viewer_script(workspace_root)
    eval_artifacts = validate_workspace_eval_artifacts(workspace_root)
    manifest_path = protocol_manifest_path(workspace_root)
    protocol_check = validate_protocol_manifest(workspace_root, manifest_path) if manifest_path.exists() else {
        "manifest_path": manifest_path.relative_to(workspace_root).as_posix(),
        "issue_count": 1,
        "issues": [{"path": manifest_path.relative_to(workspace_root).as_posix(), "problem": "missing file"}],
        "passed": False,
    }
    plan = benchmark_agent_plan(iteration_dir, baseline_isolation=baseline_isolation)

    checks = [
        {
            "name": "policy_tests",
            **policy_test,
        },
        {
            "name": "blind_isolation",
            "passed": bool(blind_isolation.get("passed")),
            "issue_count": blind_isolation.get("issue_count", 0),
        },
        {
            "name": "harness_tests",
            **harness_test,
        },
        {
            "name": "eval_artifacts",
            "passed": bool(eval_artifacts.get("passed")),
            "issue_count": eval_artifacts.get("issue_count", 0),
        },
        {
            "name": "protocol_manifest",
            "passed": bool(protocol_check.get("passed")),
            "issue_count": protocol_check.get("issue_count", 0),
        },
        {
            "name": "workspace_skill_creator",
            "passed": True,
            "path": viewer_script.relative_to(workspace_root).as_posix(),
        },
    ]

    return {
        "iteration": iteration_dir.name,
        "baseline_isolation": baseline_isolation,
        "interactive_entrypoint": INTERACTIVE_ENTRYPOINT,
        "automation_entrypoint": AUTOMATION_ENTRYPOINT,
        "checks": checks,
        "policy_test": policy_test,
        "harness_test": harness_test,
        "blind_isolation": blind_isolation,
        "eval_artifacts": eval_artifacts,
        "protocol_manifest": protocol_check,
        "agent_plan": plan,
        "passed": all(check.get("passed") for check in checks),
    }


def validate_run_metrics_payload(metrics: dict[str, Any]) -> list[str]:
    return [key for key in REQUIRED_RUN_METRIC_KEYS if key not in metrics or metrics[key] is None]


def validate_iteration_metrics(iteration_dir: Path) -> dict[str, Any]:
    issues: list[dict[str, Any]] = []
    normalized_files: list[dict[str, Any]] = []
    expected_files = len(skill_dirs(iteration_dir)) * 2
    checked_files = 0

    for skill_dir in skill_dirs(iteration_dir):
        for config in ("with_skill", "without_skill"):
            metrics_path = skill_dir / f"{config}-run-metrics.json"
            relative_path = metrics_path.relative_to(iteration_dir).as_posix()
            if not metrics_path.exists():
                issues.append(
                    {
                        "skill": skill_dir.name,
                        "configuration": config,
                        "path": relative_path,
                        "problem": "missing-file",
                    }
                )
                continue

            checked_files += 1
            metrics, changes = load_run_metrics(metrics_path, write_back=True)
            if changes:
                normalized_files.append(
                    {
                        "skill": skill_dir.name,
                        "configuration": config,
                        "path": relative_path,
                        "changes": changes,
                    }
                )
            missing_keys = validate_run_metrics_payload(metrics)
            if missing_keys:
                issues.append(
                    {
                        "skill": skill_dir.name,
                        "configuration": config,
                        "path": relative_path,
                        "problem": "missing-or-null-keys",
                        "missing_keys": missing_keys,
                    }
                )
            for run_entry in metrics.get("runs", []) if isinstance(metrics.get("runs"), list) else []:
                if not isinstance(run_entry, dict):
                    issues.append(
                        {
                            "skill": skill_dir.name,
                            "configuration": config,
                            "path": relative_path,
                            "problem": "invalid-run-entry",
                        }
                    )
                    continue
                run_missing_keys = validate_run_metrics_payload(run_entry)
                if run_missing_keys:
                    issues.append(
                        {
                            "skill": skill_dir.name,
                            "configuration": config,
                            "path": relative_path,
                            "problem": "missing-or-null-run-keys",
                            "run_number": run_entry.get("run_number"),
                            "missing_keys": run_missing_keys,
                        }
                    )

    summary = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "iteration": iteration_dir.name,
        "status": "passed" if not issues else "failed",
        "expected_files": expected_files,
        "checked_files": checked_files,
        "normalized_file_count": len(normalized_files),
        "normalized_files": normalized_files,
        "issue_count": len(issues),
        "issues": issues,
    }
    write_json(iteration_dir / "_meta" / "metric-validation.json", summary)
    return summary


def pre_aggregate_check(iteration_dir: Path, workspace_root: Path) -> dict[str, Any]:
    issues: list[dict[str, Any]] = []
    checked_files = 0
    required_files = (
        "with_skill-run-metrics.json",
        "without_skill-run-metrics.json",
        "with_skill-summary.json",
        "without_skill-summary.json",
        "blind-comparisons.json",
    )

    for skill_dir in skill_dirs(iteration_dir):
        for filename in required_files:
            path = skill_dir / filename
            relative_path = path.relative_to(workspace_root).as_posix()
            if not path.exists():
                issues.append(
                    {
                        "skill": skill_dir.name,
                        "file": filename,
                        "path": relative_path,
                        "reason": "missing-file",
                    }
                )
                continue

            checked_files += 1
            try:
                payload = read_json(path)
            except Exception as exc:
                issues.append(
                    {
                        "skill": skill_dir.name,
                        "file": filename,
                        "path": relative_path,
                        "reason": "invalid-json",
                        "details": str(exc),
                    }
                )
                continue

            if filename.endswith("-run-metrics.json"):
                if not isinstance(payload, dict):
                    issues.append(
                        {
                            "skill": skill_dir.name,
                            "file": filename,
                            "path": relative_path,
                            "reason": "invalid-run-metrics-payload",
                            "details": f"expected JSON object, got {type(payload).__name__}",
                        }
                    )
                    continue
                missing_keys = validate_run_metrics_payload(payload)
                if missing_keys:
                    issues.append(
                        {
                            "skill": skill_dir.name,
                            "file": filename,
                            "path": relative_path,
                            "reason": "missing-or-null-keys",
                            "missing_keys": missing_keys,
                        }
                    )
                runs = payload.get("runs")
                if not isinstance(runs, list) or not runs:
                    issues.append(
                        {
                            "skill": skill_dir.name,
                            "file": filename,
                            "path": relative_path,
                            "reason": "missing-runs-array",
                        }
                    )
                    continue
                for run_entry in runs:
                    if not isinstance(run_entry, dict):
                        issues.append(
                            {
                                "skill": skill_dir.name,
                                "file": filename,
                                "path": relative_path,
                                "reason": "invalid-run-entry",
                            }
                        )
                        continue
                    run_missing_keys = validate_run_metrics_payload(run_entry)
                    if run_missing_keys:
                        issues.append(
                            {
                                "skill": skill_dir.name,
                                "file": filename,
                                "path": relative_path,
                                "reason": "missing-or-null-run-keys",
                                "run_number": run_entry.get("run_number"),
                                "missing_keys": run_missing_keys,
                            }
                        )
            elif filename == "blind-comparisons.json":
                try:
                    comparisons = load_comparisons(path)
                    for item in comparisons:
                        normalize_comparison_entry(item)
                except Exception as exc:
                    issues.append(
                        {
                            "skill": skill_dir.name,
                            "file": filename,
                            "path": relative_path,
                            "reason": "invalid-comparison-schema",
                            "details": str(exc),
                        }
                    )

    summary = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "iteration": iteration_dir.name,
        "status": "ok" if not issues else "fail",
        "skill_count": len(skill_dirs(iteration_dir)),
        "checked_files": checked_files,
        "issues": issues,
        "issue_count": len(issues),
    }
    write_json(iteration_dir / "_meta" / "pre-aggregate-check.json", summary)
    return summary


def normalize_iteration_metrics(iteration_dir: Path) -> dict[str, Any]:
    normalized_files: list[dict[str, Any]] = []
    checked_files = 0

    for skill_dir in skill_dirs(iteration_dir):
        for config in ("with_skill", "without_skill"):
            metrics_path = skill_dir / f"{config}-run-metrics.json"
            if not metrics_path.exists():
                continue
            checked_files += 1
            metrics, changes = load_run_metrics(metrics_path, write_back=True)
            if changes:
                normalized_files.append(
                    {
                        "skill": skill_dir.name,
                        "configuration": config,
                        "path": metrics_path.relative_to(iteration_dir).as_posix(),
                        "changes": changes,
                        "required_keys_present": len(validate_run_metrics_payload(metrics)) == 0,
                    }
                )

    summary = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "iteration": iteration_dir.name,
        "checked_files": checked_files,
        "normalized_file_count": len(normalized_files),
        "normalized_files": normalized_files,
    }
    write_json(iteration_dir / "_meta" / "metric-normalization.json", summary)
    return summary


def clean_benchmark_artifacts(workspace_root: Path) -> dict[str, Any]:
    return _clean_benchmark_artifacts(workspace_root)


def prune_generated_artifacts(iteration_dir: Path, workspace_root: Path) -> dict[str, Any]:
    return _prune_generated_artifacts(iteration_dir, workspace_root)


def current_utc_timestamp() -> dict[str, Any]:
    return {
        "timestamp": utc_now_iso(),
    }


def prepare_blind(iteration_dir: Path) -> dict[str, Any]:
    prepared: list[dict[str, Any]] = []
    for skill_dir in skill_dirs(iteration_dir):
        for eval_dir in sorted(skill_dir.glob("eval-*"), key=lambda path: path.name):
            eval_id = int(eval_dir.name.split("-", 1)[1])
            run_numbers = sorted(
                set(discover_run_numbers(skill_dir, "with_skill"))
                & set(discover_run_numbers(skill_dir, "without_skill"))
            )
            for run_number in run_numbers:
                with_response = resolve_response_path(skill_dir, eval_id, "with_skill", run_number)
                without_response = resolve_response_path(skill_dir, eval_id, "without_skill", run_number)
                if with_response is None or without_response is None:
                    continue

                blind_dir = blind_dir_for_run(eval_dir, run_number)
                blind_dir.mkdir(parents=True, exist_ok=True)

                seed = hashlib.sha256(
                    f"{iteration_dir.name}:{skill_dir.name}:{eval_dir.name}:{run_label(run_number)}".encode("utf-8")
                ).hexdigest()
                swap = int(seed[:2], 16) % 2 == 1
                mapping = {
                    "A": "without_skill" if swap else "with_skill",
                    "B": "with_skill" if swap else "without_skill",
                }
                source_by_config = {
                    "with_skill": with_response,
                    "without_skill": without_response,
                }

                write_text(blind_dir / "A.md", source_by_config[mapping["A"]].read_text(encoding="utf-8"))
                write_text(blind_dir / "B.md", source_by_config[mapping["B"]].read_text(encoding="utf-8"))
                write_json(blind_map_path(eval_dir, run_number), mapping)

                prepared.append(
                    {
                        "skill": skill_dir.name,
                        "eval": eval_dir.name,
                        "run_number": run_number,
                        "mapping": mapping,
                    }
                )

    summary = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "iteration": iteration_dir.name,
        "prepared": prepared,
        "prepared_count": len(prepared),
    }
    write_json(iteration_dir / "_meta" / "blind-preparation.json", summary)
    return summary


def load_comparisons(path: Path) -> list[dict[str, Any]]:
    data = read_json(path)
    if isinstance(data, dict):
        return data.get("comparisons", [])
    if isinstance(data, list):
        return data
    raise ValueError(f"Unsupported comparison format in {path}")


def iteration_caveats_path(iteration_dir: Path) -> Path:
    return iteration_dir / "_meta" / ITERATION_CAVEATS_FILENAME


def load_iteration_caveats(iteration_dir: Path) -> dict[str, Any] | None:
    path = iteration_caveats_path(iteration_dir)
    if not path.exists():
        return None
    data = read_json(path)
    if not isinstance(data, dict):
        raise ValueError(f"Iteration caveats must be a JSON object: {path}")
    return data


def derive_iteration_comparison_validity(caveats: dict[str, Any] | None) -> dict[str, Any]:
    caveats = caveats if isinstance(caveats, dict) else {}

    reused_blind_from = caveats.get("reused_blind_comparisons_from_iteration")
    if not isinstance(reused_blind_from, str) or not reused_blind_from.strip():
        reused_blind_from = None

    synthetic_timing = bool(caveats.get("synthetic_timing"))
    injected_guidance = bool(caveats.get("with_skill_guidance_injected"))
    notes = normalize_string_list(caveats.get("notes", []))

    reasons: list[str] = []
    protocol_deviations: list[str] = []

    if reused_blind_from:
        reasons.append(
            f"Blind comparison results were reused from {reused_blind_from}, so blind-derived metrics do not describe fresh A/B judgments for this iteration."
        )
    if synthetic_timing:
        reasons.append("Timing metrics use synthetic placeholder values, so time comparisons are not trustworthy.")
    if injected_guidance:
        protocol_deviations.append(
            "with_skill responses were produced with injected target-skill guidance rather than a clean targeted worker session."
        )

    return {
        "provisional": bool(reasons or protocol_deviations or notes),
        "blind_metrics_trustworthy": reused_blind_from is None,
        "time_metrics_trustworthy": not synthetic_timing,
        "previous_iteration_comparison_trustworthy": not (reused_blind_from or synthetic_timing or injected_guidance),
        "reasons": reasons,
        "protocol_deviations": protocol_deviations,
        "notes": notes,
    }


def apply_iteration_comparison_validity(skill_rows: list[dict[str, Any]], validity: dict[str, Any]) -> None:
    if not validity.get("blind_metrics_trustworthy", True):
        for skill in skill_rows:
            blind = skill.get("capability", {}).get("blind", {})
            blind["with_skill_win_rate"] = None
            blind["without_skill_win_rate"] = None
            blind["variance"] = {
                "with_skill_win_rate": None,
                "without_skill_win_rate": None,
            }

            expectation = skill.get("capability", {}).get("expectation_pass_rate", {})
            expectation["with_skill"] = None
            expectation["without_skill"] = None
            expectation["delta"] = None
            expectation["variance"] = {
                "with_skill": None,
                "without_skill": None,
                "delta": None,
            }

            rubric = skill.get("capability", {}).get("rubric_score", {})
            rubric["with_skill"] = None
            rubric["without_skill"] = None
            rubric["delta"] = None
            rubric["variance"] = {
                "with_skill": None,
                "without_skill": None,
                "delta": None,
            }

            skill.get("capability", {})["high_variance_evals"] = []
            skill["high_variance_evals"] = [
                item for item in skill.get("high_variance_evals", []) if item.get("source") != "blind"
            ]

    if not validity.get("time_metrics_trustworthy", True):
        for skill in skill_rows:
            for configuration in ("with_skill", "without_skill"):
                block = skill.get("time", {}).get(configuration, {})
                previous_variance = block.get("variance", {})
                block["elapsed_seconds_total"] = None
                block["elapsed_seconds_per_eval"] = None
                block["variance"] = {
                    "elapsed_seconds_total": None,
                    "elapsed_seconds_per_eval": None,
                    "response_words_total": previous_variance.get("response_words_total"),
                    "response_words_per_eval": previous_variance.get("response_words_per_eval"),
                    "files_read_count": previous_variance.get("files_read_count"),
                    "files_written_count": previous_variance.get("files_written_count"),
                }
            skill.get("time", {}).setdefault("delta", {})["elapsed_seconds_total"] = None
            skill.get("time", {}).setdefault("delta", {})["elapsed_seconds_per_eval"] = None


def load_likec4_reference_data(workspace_root: Path) -> dict[str, Any]:
    spec_paths = [
        workspace_root / "projects" / "shared" / name
        for name in (
            "spec-global.c4",
            "spec-context.c4",
            "spec-containers.c4",
            "spec-components.c4",
            "spec-deployment.c4",
        )
    ]
    kinds: set[str] = set()
    relationships: set[str] = set()
    for path in spec_paths:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        kinds.update(re.findall(r"^\s*element\s+([A-Za-z_][\w]*)\s*\{", text, flags=re.MULTILINE))
        kinds.update(re.findall(r"^\s*deploymentNode\s+([A-Za-z_][\w]*)\s*\{", text, flags=re.MULTILINE))
        relationships.update(re.findall(r"^\s*relationship\s+([A-Za-z_][\w]*)\s*\{", text, flags=re.MULTILINE))
    return {
        "known_kinds": sorted(kinds),
        "known_relationships": sorted(relationships),
    }


def extract_likec4_snippets(response_text: str) -> list[str]:
    snippets: list[str] = []
    fence_pattern = re.compile(r"```(?:likec4|c4|txt|text)?\n(.*?)```", re.IGNORECASE | re.DOTALL)
    for match in fence_pattern.finditer(response_text):
        snippet = match.group(1).strip()
        if snippet and any(marker in snippet for marker in ("=", "->", "view", "views", "deployment", "{")):
            snippets.append(snippet)

    if snippets:
        return snippets

    inline_candidates: list[list[str]] = []
    current: list[str] = []
    inline_pattern = re.compile(
        r"(^\s*[A-Za-z_][\w.]*\s*=\s*[A-Za-z_][\w]*\b)|(^\s*[A-Za-z_][\w.]*\s*->\s*[A-Za-z_][\w.]*\b)|(^\s*(views?|deployment|model)\b)|(^\s*[{}]\s*$)",
        re.IGNORECASE,
    )
    for line in response_text.splitlines():
        if inline_pattern.search(line):
            current.append(line)
            continue
        if current:
            inline_candidates.append(current)
            current = []
    if current:
        inline_candidates.append(current)

    for block in inline_candidates:
        snippet = "\n".join(block).strip()
        if snippet:
            snippets.append(snippet)
    return snippets


def analyze_likec4_snippet(snippet: str, reference_data: dict[str, Any]) -> dict[str, Any]:
    known_kinds = set(reference_data.get("known_kinds", []))
    known_relationships = set(reference_data.get("known_relationships", []))
    errors: list[str] = []
    warnings: list[str] = []
    declared_symbols: set[str] = set()

    brace_balance = 0
    for character in snippet:
        if character == "{":
            brace_balance += 1
        elif character == "}":
            brace_balance -= 1
        if brace_balance < 0:
            errors.append("Closing brace appears before a matching opening brace.")
            break
    if brace_balance != 0:
        errors.append("Braces are not balanced.")

    declaration_pattern = re.compile(r"^\s*([A-Za-z_][\w.]*)\s*=\s*([A-Za-z_][\w]*)\b", re.MULTILINE)
    for match in declaration_pattern.finditer(snippet):
        symbol = match.group(1)
        kind = match.group(2)
        declared_symbols.add(symbol.split(".")[-1])
        if kind not in known_kinds:
            errors.append(f"Unknown LikeC4 kind '{kind}'.")

    relationship_pattern = re.compile(r"^\s*([A-Za-z_][\w.]*)\s*->\s*([A-Za-z_][\w.]*)(.*)$", re.MULTILINE)
    for match in relationship_pattern.finditer(snippet):
        source = match.group(1)
        target = match.group(2)
        tail = match.group(3).strip()

        for endpoint in (source, target):
            leaf = endpoint.split(".")[-1]
            if "." not in endpoint and leaf not in declared_symbols:
                warnings.append(f"Reference '{endpoint}' is not declared inside the snippet (may rely on surrounding model context).")

        if tail and not tail.startswith('"') and not tail.startswith("{") and not tail.startswith("//"):
            relationship_kind = tail.split()[0]
            if relationship_kind not in known_relationships:
                errors.append(f"Unknown relationship kind '{relationship_kind}'.")

    return {
        "snippet": snippet,
        "valid": len(errors) == 0,
        "error_count": len(errors),
        "warning_count": len(warnings),
        "errors": errors,
        "warnings": warnings,
    }


def analyze_likec4_response(response_text: str, reference_data: dict[str, Any]) -> dict[str, Any]:
    snippets = extract_likec4_snippets(response_text)
    if not snippets:
        return {
            "status": "not_applicable",
            "snippet_count": 0,
            "valid_snippet_count": 0,
            "error_count": 0,
            "warning_count": 0,
            "snippets": [],
        }

    analyses = [analyze_likec4_snippet(snippet, reference_data) for snippet in snippets]
    return {
        "status": "checked",
        "snippet_count": len(analyses),
        "valid_snippet_count": sum(1 for item in analyses if item["valid"]),
        "error_count": sum(item["error_count"] for item in analyses),
        "warning_count": sum(item["warning_count"] for item in analyses),
        "snippets": analyses,
    }


def validate_executable_checks(iteration_dir: Path, workspace_root: Path) -> dict[str, Any]:
    reference_data = load_likec4_reference_data(workspace_root)
    summaries: list[dict[str, Any]] = []

    for skill_dir in skill_dirs(iteration_dir):
        eval_definition = load_skill_eval_public_definition(workspace_root, skill_dir.name)
        eval_ids = [item.get("id") for item in eval_definition.get("evals", []) if isinstance(item.get("id"), int)]
        for configuration in ("with_skill", "without_skill"):
            run_numbers = discover_run_numbers(skill_dir, configuration)
            eval_results: list[dict[str, Any]] = []
            applicable_eval_count = 0
            valid_eval_count = 0
            snippet_count_total = 0
            error_count_total = 0
            warning_count_total = 0

            for run_number in run_numbers:
                for eval_id in eval_ids:
                    response_path = resolve_response_path(skill_dir, int(eval_id), configuration, run_number)
                    if response_path is None:
                        continue
                    analysis = analyze_likec4_response(response_path.read_text(encoding="utf-8"), reference_data)
                    if analysis["status"] == "checked":
                        applicable_eval_count += 1
                        if analysis["error_count"] == 0:
                            valid_eval_count += 1
                    snippet_count_total += analysis["snippet_count"]
                    error_count_total += analysis["error_count"]
                    warning_count_total += analysis["warning_count"]
                    eval_results.append(
                        {
                            "id": eval_id,
                            "run_number": run_number,
                            "response_path": response_path.relative_to(skill_dir).as_posix(),
                            **analysis,
                        }
                    )

            summary = {
                "iteration": iteration_dir.name,
                "skill_name": skill_dir.name,
                "configuration": configuration,
                "checked_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "run_count": len(run_numbers),
                "summary": {
                    "applicable_eval_count": applicable_eval_count,
                    "valid_eval_count": valid_eval_count,
                    "valid_eval_rate": round(valid_eval_count / applicable_eval_count, 4) if applicable_eval_count else None,
                    "snippet_count_total": snippet_count_total,
                    "error_count_total": error_count_total,
                    "warning_count_total": warning_count_total,
                },
                "evals": eval_results,
            }
            output_path = skill_dir / f"{configuration}-executable-checks.json"
            write_json(output_path, summary)
            summaries.append(
                {
                    "skill": skill_dir.name,
                    "configuration": configuration,
                    "output_path": output_path.relative_to(workspace_root).as_posix(),
                    "applicable_eval_count": applicable_eval_count,
                    "valid_eval_rate": summary["summary"]["valid_eval_rate"],
                }
            )

    report = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "iteration": iteration_dir.name,
        "summary_count": len(summaries),
        "summaries": summaries,
    }
    write_json(iteration_dir / "_meta" / "executable-checks-summary.json", report)
    return report


def load_executable_check_metrics(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    data = read_json(path)
    return {
        "applicable_eval_count": data.get("summary", {}).get("applicable_eval_count"),
        "valid_eval_count": data.get("summary", {}).get("valid_eval_count"),
        "valid_eval_rate": data.get("summary", {}).get("valid_eval_rate"),
        "snippet_count_total": data.get("summary", {}).get("snippet_count_total"),
        "error_count_total": data.get("summary", {}).get("error_count_total"),
        "warning_count_total": data.get("summary", {}).get("warning_count_total"),
    }


def load_summary_metrics(path: Path) -> dict[str, Any]:
    data = read_json(path)
    summary = data.get("summary", {})
    return {
        "elapsed_seconds_total": summary.get("elapsed_seconds_total"),
        "elapsed_seconds_per_eval": summary.get("elapsed_seconds_per_eval"),
        "response_words_total": summary.get("response_words_total"),
        "response_words_per_eval": summary.get("response_words_per_eval"),
        "files_read_count": summary.get("files_read_count"),
        "files_written_count": summary.get("files_written_count"),
        "eval_count": len(data.get("evals", [])),
        "run_count": data.get("run_count", len(data.get("runs", [])) or 1),
        "variance": data.get("variance", {}),
        "high_variance_evals": data.get("high_variance_evals", []),
    }


def comparison_metrics(skill_dir: Path, comparison_items: list[dict[str, Any]]) -> dict[str, Any]:
    with_win_count = 0
    without_win_count = 0
    ties = 0
    with_win_indicators: list[float] = []
    without_win_indicators: list[float] = []
    with_expectation_rates: list[float] = []
    without_expectation_rates: list[float] = []
    expectation_deltas: list[float] = []
    with_rubric_scores: list[float] = []
    without_rubric_scores: list[float] = []
    rubric_deltas: list[float] = []
    per_eval_records: dict[int, list[dict[str, Any]]] = {}

    for item in comparison_items:
        eval_id = item.get("eval_id")
        if not isinstance(eval_id, int):
            continue
        run_number = coerce_int(item.get("run_number")) or 1
        eval_dir = skill_dir / f"eval-{eval_id}"
        mapping_path = blind_map_path(eval_dir, run_number)
        if not mapping_path.exists():
            continue
        mapping = read_json(mapping_path)
        reverse_mapping = {config: side for side, config in mapping.items()}

        winner = item.get("winner")
        winner_outcome = "TIE"
        if winner == "TIE":
            ties += 1
            with_win_indicators.append(0.0)
            without_win_indicators.append(0.0)
        elif mapping.get(winner) == "with_skill":
            with_win_count += 1
            with_win_indicators.append(1.0)
            without_win_indicators.append(0.0)
            winner_outcome = "with_skill"
        elif mapping.get(winner) == "without_skill":
            without_win_count += 1
            with_win_indicators.append(0.0)
            without_win_indicators.append(1.0)
            winner_outcome = "without_skill"

        expectation_results = item.get("expectation_results", {})
        rubric = item.get("rubric", {})

        with_side = reverse_mapping.get("with_skill")
        without_side = reverse_mapping.get("without_skill")

        with_expectation_rate = None
        without_expectation_rate = None
        if with_side and with_side in expectation_results:
            with_expectation_rate = expectation_results[with_side].get("pass_rate", 0.0)
            with_expectation_rates.append(with_expectation_rate)
        if without_side and without_side in expectation_results:
            without_expectation_rate = expectation_results[without_side].get("pass_rate", 0.0)
            without_expectation_rates.append(without_expectation_rate)

        with_rubric_score = None
        without_rubric_score = None
        if with_side and with_side in rubric:
            with_rubric_score = rubric[with_side].get("overall_score", 0.0)
            with_rubric_scores.append(with_rubric_score)
        if without_side and without_side in rubric:
            without_rubric_score = rubric[without_side].get("overall_score", 0.0)
            without_rubric_scores.append(without_rubric_score)

        expectation_delta = None
        if with_expectation_rate is not None and without_expectation_rate is not None:
            expectation_delta = round(float(with_expectation_rate) - float(without_expectation_rate), 4)
            expectation_deltas.append(expectation_delta)

        rubric_delta = None
        if with_rubric_score is not None and without_rubric_score is not None:
            rubric_delta = round(float(with_rubric_score) - float(without_rubric_score), 4)
            rubric_deltas.append(rubric_delta)

        per_eval_records.setdefault(eval_id, []).append(
            {
                "run_number": run_number,
                "winner_outcome": winner_outcome,
                "with_expectation_rate": with_expectation_rate,
                "without_expectation_rate": without_expectation_rate,
                "expectation_delta": expectation_delta,
                "with_rubric_score": with_rubric_score,
                "without_rubric_score": without_rubric_score,
                "rubric_delta": rubric_delta,
            }
        )

    total_resolved = with_win_count + without_win_count + ties
    with_win_rate = (with_win_count / total_resolved) if total_resolved else None
    without_win_rate = (without_win_count / total_resolved) if total_resolved else None

    with_expectation_mean = safe_mean(with_expectation_rates)
    without_expectation_mean = safe_mean(without_expectation_rates)
    with_rubric_mean = safe_mean(with_rubric_scores)
    without_rubric_mean = safe_mean(without_rubric_scores)

    per_eval_variance: list[dict[str, Any]] = []
    high_variance_evals: list[dict[str, Any]] = []
    for eval_id, records in sorted(per_eval_records.items()):
        expectation_delta_values = [value["expectation_delta"] for value in records if value.get("expectation_delta") is not None]
        rubric_delta_values = [value["rubric_delta"] for value in records if value.get("rubric_delta") is not None]
        winner_outcomes = sorted({value["winner_outcome"] for value in records})
        entry = {
            "id": eval_id,
            "run_count": len(records),
            "winner_outcomes": winner_outcomes,
            "winner_flips": len(winner_outcomes) > 1,
            "expectation_delta_stats": calculate_benchmark_stats(expectation_delta_values) if expectation_delta_values else None,
            "rubric_delta_stats": calculate_benchmark_stats(rubric_delta_values) if rubric_delta_values else None,
        }
        per_eval_variance.append(entry)
        expectation_stddev = entry["expectation_delta_stats"]["stddev"] if entry["expectation_delta_stats"] else 0.0
        rubric_stddev = entry["rubric_delta_stats"]["stddev"] if entry["rubric_delta_stats"] else 0.0
        if entry["winner_flips"] or expectation_stddev >= HIGH_VARIANCE_EXPECTATION_STDDEV or rubric_stddev >= HIGH_VARIANCE_RUBRIC_STDDEV:
            high_variance_evals.append(entry)

    return {
        "blind": {
            "with_skill_wins": with_win_count,
            "without_skill_wins": without_win_count,
            "ties": ties,
            "with_skill_win_rate": round_or_none(with_win_rate),
            "without_skill_win_rate": round_or_none(without_win_rate),
            "variance": {
                "with_skill_win_rate": calculate_benchmark_stats(with_win_indicators) if with_win_indicators else None,
                "without_skill_win_rate": calculate_benchmark_stats(without_win_indicators) if without_win_indicators else None,
            },
        },
        "expectation_pass_rate": {
            "with_skill": with_expectation_mean,
            "without_skill": without_expectation_mean,
            "delta": delta_or_none(with_expectation_mean, without_expectation_mean),
            "variance": {
                "with_skill": calculate_benchmark_stats(with_expectation_rates) if with_expectation_rates else None,
                "without_skill": calculate_benchmark_stats(without_expectation_rates) if without_expectation_rates else None,
                "delta": calculate_benchmark_stats(expectation_deltas) if expectation_deltas else None,
            },
        },
        "rubric_score": {
            "with_skill": with_rubric_mean,
            "without_skill": without_rubric_mean,
            "delta": delta_or_none(with_rubric_mean, without_rubric_mean),
            "variance": {
                "with_skill": calculate_benchmark_stats(with_rubric_scores) if with_rubric_scores else None,
                "without_skill": calculate_benchmark_stats(without_rubric_scores) if without_rubric_scores else None,
                "delta": calculate_benchmark_stats(rubric_deltas) if rubric_deltas else None,
            },
        },
        "comparison_count": total_resolved,
        "per_eval_variance": per_eval_variance,
        "high_variance_evals": high_variance_evals,
    }


def build_skill_row_with_reason(skill_dir: Path, workspace_root: Path) -> tuple[dict[str, Any] | None, str | None]:
    with_summary_path = skill_dir / "with_skill-summary.json"
    without_summary_path = skill_dir / "without_skill-summary.json"
    comparisons_path = skill_dir / "blind-comparisons.json"

    missing_paths = [
        path.name
        for path in (with_summary_path, without_summary_path, comparisons_path)
        if not path.exists()
    ]
    if missing_paths:
        return None, f"missing required artifacts: {', '.join(missing_paths)}"

    try:
        eval_bundle = load_skill_eval_bundle(workspace_root, skill_dir.name)
    except Exception as exc:
        return None, f"failed to load eval bundle: {exc}"

    with_metrics = load_summary_metrics(with_summary_path)
    without_metrics = load_summary_metrics(without_summary_path)
    comparison_items = load_comparisons(comparisons_path)
    capability = comparison_metrics(skill_dir, comparison_items)
    eval_def = eval_bundle["public"]
    eval_count = len(eval_def.get("evals", []))
    with_executable = load_executable_check_metrics(skill_dir / "with_skill-executable-checks.json")
    without_executable = load_executable_check_metrics(skill_dir / "without_skill-executable-checks.json")

    high_variance_evals = []
    seen_variance_keys: set[tuple[str, int]] = set()
    for source, metrics in (("with_skill", with_metrics), ("without_skill", without_metrics)):
        for item in metrics.get("high_variance_evals", []):
            eval_id = coerce_int(item.get("id"))
            if eval_id is None:
                continue
            key = (source, eval_id)
            if key not in seen_variance_keys:
                seen_variance_keys.add(key)
                high_variance_evals.append({"source": source, **item})
    for item in capability.get("high_variance_evals", []):
        eval_id = coerce_int(item.get("id"))
        key = ("blind", eval_id or -1)
        if key not in seen_variance_keys:
            seen_variance_keys.add(key)
            high_variance_evals.append({"source": "blind", **item})

    return {
        "skill": skill_dir.name,
        "eval_count": eval_count,
        "run_count": max(with_metrics.get("run_count", 1), without_metrics.get("run_count", 1)),
        "capability": capability,
        "consumption": {
            "with_skill": {
                "response_words_per_eval": with_metrics.get("response_words_per_eval"),
                "files_read_count": with_metrics.get("files_read_count"),
                "files_written_count": with_metrics.get("files_written_count"),
                "variance": with_metrics.get("variance", {}),
            },
            "without_skill": {
                "response_words_per_eval": without_metrics.get("response_words_per_eval"),
                "files_read_count": without_metrics.get("files_read_count"),
                "files_written_count": without_metrics.get("files_written_count"),
                "variance": without_metrics.get("variance", {}),
            },
            "delta": {
                "response_words_per_eval": delta_or_none(with_metrics.get("response_words_per_eval"), without_metrics.get("response_words_per_eval")),
                "files_read_count": delta_or_none(with_metrics.get("files_read_count"), without_metrics.get("files_read_count")),
                "files_written_count": delta_or_none(with_metrics.get("files_written_count"), without_metrics.get("files_written_count")),
            },
        },
        "time": {
            "with_skill": {
                "elapsed_seconds_total": with_metrics.get("elapsed_seconds_total"),
                "elapsed_seconds_per_eval": with_metrics.get("elapsed_seconds_per_eval"),
                "variance": with_metrics.get("variance", {}),
            },
            "without_skill": {
                "elapsed_seconds_total": without_metrics.get("elapsed_seconds_total"),
                "elapsed_seconds_per_eval": without_metrics.get("elapsed_seconds_per_eval"),
                "variance": without_metrics.get("variance", {}),
            },
            "delta": {
                "elapsed_seconds_total": delta_or_none(with_metrics.get("elapsed_seconds_total"), without_metrics.get("elapsed_seconds_total")),
                "elapsed_seconds_per_eval": delta_or_none(with_metrics.get("elapsed_seconds_per_eval"), without_metrics.get("elapsed_seconds_per_eval")),
            },
        },
        "executable_validity": {
            "with_skill": with_executable,
            "without_skill": without_executable,
            "delta": {
                "valid_eval_rate": delta_or_none(
                    with_executable.get("valid_eval_rate") if with_executable else None,
                    without_executable.get("valid_eval_rate") if without_executable else None,
                ),
            },
        },
        "high_variance_evals": high_variance_evals,
    }, None


def build_skill_row(skill_dir: Path, workspace_root: Path) -> dict[str, Any] | None:
	row, _reason = build_skill_row_with_reason(skill_dir, workspace_root)
	return row


def suite_overview_rows(skill_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for row in skill_rows:
        rows.append(
            {
                "skill": row["skill"],
                "eval_count": row["eval_count"],
                "with_skill_win_rate": row["capability"]["blind"]["with_skill_win_rate"],
                "expectation_delta": row["capability"]["expectation_pass_rate"]["delta"],
                "rubric_delta": row["capability"]["rubric_score"]["delta"],
                "time_delta_per_eval": row["time"]["delta"]["elapsed_seconds_per_eval"],
                "words_delta_per_eval": row["consumption"]["delta"]["response_words_per_eval"],
                "files_read_delta": row["consumption"]["delta"]["files_read_count"],
                "executable_delta": row["executable_validity"]["delta"]["valid_eval_rate"],
                "run_count": row.get("run_count", 1),
                "high_variance_eval_count": len(row.get("high_variance_evals", [])),
            }
        )
    return rows


def summarize_config(skill_dir: Path, config: str, evals_path: Path, metrics_path: Path | None = None) -> dict[str, Any]:
    eval_definition = read_json(evals_path)
    metrics_file = metrics_path or (skill_dir / f"{config}-run-metrics.json")
    if not metrics_file.exists():
        raise FileNotFoundError(f"Missing run metrics for {skill_dir.name} {config}: {metrics_file}")

    metrics, _changes = load_run_metrics(metrics_file, write_back=True)
    missing_metric_keys = validate_run_metrics_payload(metrics)
    if missing_metric_keys:
        raise ValueError(
            f"Incomplete run metrics for {skill_dir.name} {config}: missing/null keys {missing_metric_keys} in {metrics_file}"
        )

    run_entries = metrics.get("runs") if isinstance(metrics.get("runs"), list) and metrics.get("runs") else [metrics]
    run_summaries: list[dict[str, Any]] = []
    response_word_samples: dict[int, list[float]] = {}

    for index, run_metrics in enumerate(run_entries, start=1):
        run_number = coerce_int(run_metrics.get("run_number")) or index
        eval_rows: list[dict[str, Any]] = []
        total_words = 0

        for eval_item in eval_definition.get("evals", []):
            eval_id = eval_item.get("id")
            response_path = resolve_response_path(skill_dir, int(eval_id), config, run_number) if eval_id is not None else None
            if response_path is None:
                raise FileNotFoundError(
                    f"Missing response for {skill_dir.name} {config} eval-{eval_id} run-{run_number}"
                )

            response_text = response_path.read_text(encoding="utf-8")
            response_words = count_words(response_text)
            total_words += response_words
            response_word_samples.setdefault(int(eval_id), []).append(float(response_words))
            eval_rows.append(
                {
                    "id": eval_id,
                    "run_number": run_number,
                    "response_path": response_path.relative_to(skill_dir).as_posix(),
                    "response_words": response_words,
                }
            )

        eval_count = len(eval_rows)
        elapsed_seconds_total = coerce_float(run_metrics.get("elapsed_seconds_total"))
        elapsed_seconds_per_eval = None
        if elapsed_seconds_total is not None and eval_count:
            elapsed_seconds_per_eval = round(float(elapsed_seconds_total) / eval_count, 4)

        run_summaries.append(
            {
                "run_number": run_number,
                "summary": {
                    "elapsed_seconds_total": round_or_none(elapsed_seconds_total),
                    "elapsed_seconds_per_eval": elapsed_seconds_per_eval,
                    "response_words_total": total_words,
                    "response_words_per_eval": round_or_none(total_words / eval_count) if eval_count else None,
                    "files_read_count": run_metrics.get("files_read_count"),
                    "files_written_count": run_metrics.get("files_written_count"),
                },
                "evals": eval_rows,
            }
        )

    def collect_summary_metric(metric_name: str) -> list[float]:
        values: list[float] = []
        for run in run_summaries:
            value = coerce_float(run.get("summary", {}).get(metric_name))
            if value is not None:
                values.append(value)
        return values

    aggregate_summary = {
        "elapsed_seconds_total": safe_mean(collect_summary_metric("elapsed_seconds_total")),
        "elapsed_seconds_per_eval": safe_mean(collect_summary_metric("elapsed_seconds_per_eval")),
        "response_words_total": safe_mean(collect_summary_metric("response_words_total")),
        "response_words_per_eval": safe_mean(collect_summary_metric("response_words_per_eval")),
        "files_read_count": safe_mean(collect_summary_metric("files_read_count")),
        "files_written_count": safe_mean(collect_summary_metric("files_written_count")),
    }
    variance = {
        metric_name: calculate_benchmark_stats(values)
        for metric_name, values in (
            ("elapsed_seconds_total", collect_summary_metric("elapsed_seconds_total")),
            ("elapsed_seconds_per_eval", collect_summary_metric("elapsed_seconds_per_eval")),
            ("response_words_total", collect_summary_metric("response_words_total")),
            ("response_words_per_eval", collect_summary_metric("response_words_per_eval")),
            ("files_read_count", collect_summary_metric("files_read_count")),
            ("files_written_count", collect_summary_metric("files_written_count")),
        )
        if values
    }
    high_variance_evals = []
    for eval_id, values in sorted(response_word_samples.items()):
        if len(values) < 2:
            continue
        stats = calculate_benchmark_stats(values)
        if stats["stddev"] >= 20.0:
            high_variance_evals.append(
                {
                    "id": eval_id,
                    "metric": "response_words",
                    "stats": stats,
                }
            )

    summary = {
        "skill_name": metrics.get("skill_name", skill_dir.name),
        "configuration": metrics.get("configuration", config),
        "language": metrics.get("language", "English"),
        "mcp_used": bool(metrics.get("mcp_used", False)),
        "run_count": len(run_summaries),
        "summary": aggregate_summary,
        "variance": variance,
        "runs": run_summaries,
        "evals": run_summaries[0]["evals"] if run_summaries else [],
        "high_variance_evals": high_variance_evals,
    }

    write_json(skill_dir / f"{config}-summary.json", summary)
    return summary


def aggregate_suite(iteration_dir: Path, workspace_root: Path) -> dict[str, Any]:
    test_root = iteration_dir.parent
    previous_iteration = find_previous_iteration(test_root, iteration_dir)
    previous_summary_path = previous_iteration / "suite-summary.json" if previous_iteration else None
    previous_summary = read_json(previous_summary_path) if previous_summary_path and previous_summary_path.exists() else None
    metric_validation = validate_iteration_metrics(iteration_dir)
    executable_validation = validate_executable_checks(iteration_dir, workspace_root)
    protocol_lock_path = iteration_dir / "_meta" / "protocol-lock.json"
    protocol_lock = read_json(protocol_lock_path) if protocol_lock_path.exists() else None
    benchmark_caveats = load_iteration_caveats(iteration_dir)
    comparison_validity = derive_iteration_comparison_validity(benchmark_caveats)

    skill_rows: list[dict[str, Any]] = []
    skipped_skills: list[dict[str, Any]] = []
    for skill_dir in skill_dirs(iteration_dir):
        row, reason = build_skill_row_with_reason(skill_dir, workspace_root)
        if row is None:
            skipped_entry = {
                "skill": skill_dir.name,
                "reason": reason or "unknown-skip-reason",
            }
            skipped_skills.append(skipped_entry)
            print(
                f"[aggregate] Skipping {skill_dir.name}: {skipped_entry['reason']}",
                file=sys.stderr,
            )
            continue
        skill_rows.append(row)
    apply_iteration_comparison_validity(skill_rows, comparison_validity)
    overview_rows = suite_overview_rows(skill_rows)

    suite_summary = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "iteration": iteration_dir.name,
        "previous_iteration": previous_iteration.name if previous_iteration else None,
        "protocol_version": protocol_lock.get("protocol_version") if protocol_lock else None,
        "protocol_lock_path": protocol_lock_path.relative_to(workspace_root).as_posix() if protocol_lock else None,
        "skill_count": len(skill_rows),
        "benchmark_caveats": benchmark_caveats,
        "comparison_validity": comparison_validity,
        "suite_averages": {
            "with_skill_win_rate": safe_mean([row["capability"]["blind"]["with_skill_win_rate"] for row in skill_rows]),
            "expectation_delta": safe_mean([row["capability"]["expectation_pass_rate"]["delta"] for row in skill_rows]),
            "rubric_delta": safe_mean([row["capability"]["rubric_score"]["delta"] for row in skill_rows]),
            "time_delta_per_eval": safe_mean([row["time"]["delta"]["elapsed_seconds_per_eval"] for row in skill_rows]),
            "words_delta_per_eval": safe_mean([row["consumption"]["delta"]["response_words_per_eval"] for row in skill_rows]),
            "files_read_delta": safe_mean([row["consumption"]["delta"]["files_read_count"] for row in skill_rows]),
            "executable_delta": safe_mean([row["executable_validity"]["delta"]["valid_eval_rate"] for row in skill_rows]),
        },
        "suite_variance": {
            "with_skill_win_rate": calculate_benchmark_stats([row["capability"]["blind"]["with_skill_win_rate"] for row in skill_rows if row["capability"]["blind"]["with_skill_win_rate"] is not None]) if [row["capability"]["blind"]["with_skill_win_rate"] for row in skill_rows if row["capability"]["blind"]["with_skill_win_rate"] is not None] else None,
            "expectation_delta": calculate_benchmark_stats([row["capability"]["expectation_pass_rate"]["delta"] for row in skill_rows if row["capability"]["expectation_pass_rate"]["delta"] is not None]) if [row["capability"]["expectation_pass_rate"]["delta"] for row in skill_rows if row["capability"]["expectation_pass_rate"]["delta"] is not None] else None,
            "rubric_delta": calculate_benchmark_stats([row["capability"]["rubric_score"]["delta"] for row in skill_rows if row["capability"]["rubric_score"]["delta"] is not None]) if [row["capability"]["rubric_score"]["delta"] for row in skill_rows if row["capability"]["rubric_score"]["delta"] is not None] else None,
            "time_delta_per_eval": calculate_benchmark_stats([row["time"]["delta"]["elapsed_seconds_per_eval"] for row in skill_rows if row["time"]["delta"]["elapsed_seconds_per_eval"] is not None]) if [row["time"]["delta"]["elapsed_seconds_per_eval"] for row in skill_rows if row["time"]["delta"]["elapsed_seconds_per_eval"] is not None] else None,
            "executable_delta": calculate_benchmark_stats([row["executable_validity"]["delta"]["valid_eval_rate"] for row in skill_rows if row["executable_validity"]["delta"]["valid_eval_rate"] is not None]) if [row["executable_validity"]["delta"]["valid_eval_rate"] for row in skill_rows if row["executable_validity"]["delta"]["valid_eval_rate"] is not None] else None,
        },
        "metric_validation": metric_validation,
        "skipped_skills": skipped_skills,
        "executable_checks": executable_validation,
        "overview": overview_rows,
        "skills": skill_rows,
        "high_variance_evals": [
            {"skill": row["skill"], **item}
            for row in skill_rows
            for item in row.get("high_variance_evals", [])
        ],
        "previous_iteration_comparison": None,
    }

    if previous_summary:
        if not comparison_validity.get("previous_iteration_comparison_trustworthy", True):
            suite_summary["previous_iteration_comparison"] = {
                "previous_iteration": previous_iteration.name,
                "status": "suppressed",
                "reasons": comparison_validity.get("reasons", []) + comparison_validity.get("protocol_deviations", []),
            }
        else:
            previous_by_skill = {row["skill"]: row for row in previous_summary.get("overview", [])}
            comparisons = []
            for row in overview_rows:
                previous_row = previous_by_skill.get(row["skill"])
                if not previous_row:
                    continue
                comparisons.append(
                    {
                        "skill": row["skill"],
                        "previous_with_skill_win_rate": previous_row.get("with_skill_win_rate"),
                        "current_with_skill_win_rate": row.get("with_skill_win_rate"),
                        "delta_with_skill_win_rate": delta_or_none(row.get("with_skill_win_rate"), previous_row.get("with_skill_win_rate")),
                        "previous_expectation_delta": previous_row.get("expectation_delta"),
                        "current_expectation_delta": row.get("expectation_delta"),
                        "delta_expectation_delta": delta_or_none(row.get("expectation_delta"), previous_row.get("expectation_delta")),
                        "previous_rubric_delta": previous_row.get("rubric_delta"),
                        "current_rubric_delta": row.get("rubric_delta"),
                        "delta_rubric_delta": delta_or_none(row.get("rubric_delta"), previous_row.get("rubric_delta")),
                        "previous_time_delta_per_eval": previous_row.get("time_delta_per_eval"),
                        "current_time_delta_per_eval": row.get("time_delta_per_eval"),
                        "delta_time_delta_per_eval": delta_or_none(row.get("time_delta_per_eval"), previous_row.get("time_delta_per_eval")),
                    }
                )
            suite_summary["previous_iteration_comparison"] = {
                "previous_iteration": previous_iteration.name,
                "skills": comparisons,
            }

    return suite_summary


def format_number(value: Any, digits: int = 2, percentage: bool = False) -> str:
    return _format_number(value, digits=digits, percentage=percentage)


def markdown_table(headers: list[str], rows: list[list[str]]) -> str:
    return _markdown_table(headers, rows)


def render_markdown(summary: dict[str, Any]) -> str:
    return _render_markdown(summary)


def cmd_prepare_blind(args: argparse.Namespace) -> None:
    summary = prepare_blind(args.iteration)
    print(json.dumps(summary, indent=2, ensure_ascii=False))


def cmd_disable_workspace_skills(args: argparse.Namespace) -> None:
    summary = disable_workspace_skills(args.workspace_root, args.iteration)
    print(json.dumps(summary, indent=2, ensure_ascii=False))


def cmd_restore_workspace_skills(args: argparse.Namespace) -> None:
    summary = restore_workspace_skills(args.workspace_root, args.iteration)
    print(json.dumps(summary, indent=2, ensure_ascii=False))


def cmd_reset_debug_log(args: argparse.Namespace) -> None:
    args.path.parent.mkdir(parents=True, exist_ok=True)
    args.path.write_text("", encoding="utf-8")
    print(json.dumps({
        "path": str(args.path),
        "cleared": True,
    }, indent=2, ensure_ascii=False))

def cmd_debug_log_window(args: argparse.Namespace) -> None:
    if not args.path.exists():
        raise FileNotFoundError(f"Missing debug log: {args.path}")

    entries: list[dict[str, Any]] = []
    for raw_line in args.path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line:
            continue
        entries.append(json.loads(line))

    worker_modes = {"baseline", "with_skill_targeted", "blind_compare", "baseline_hook_only"}
    filtered_entries = [entry for entry in entries if entry.get("mode") in worker_modes]
    timestamps = [entry.get("timestamp") for entry in filtered_entries if isinstance(entry.get("timestamp"), str) and entry.get("timestamp", "").strip()]
    print(json.dumps({
        "path": str(args.path),
        "entry_count": len(filtered_entries),
        "first_timestamp": timestamps[0] if timestamps else None,
        "last_timestamp": timestamps[-1] if timestamps else None,
        "tool_names": [entry.get("tool_name") for entry in filtered_entries],
        "paths": [entry.get("tool_paths", []) for entry in filtered_entries],
    }, indent=2, ensure_ascii=False))


def cmd_validate_hook_audit(args: argparse.Namespace) -> None:
    summary = validate_hook_audit(args.path, args.mode)
    print(json.dumps(summary, indent=2, ensure_ascii=False))


def cmd_reset_hook_state(args: argparse.Namespace) -> None:
    summary = reset_hook_state(args.workspace_root, mode=args.mode, session_id=args.session_id)
    print(json.dumps(summary, indent=2, ensure_ascii=False))


def cmd_write_protocol_manifest(args: argparse.Namespace) -> None:
    manifest = build_protocol_manifest(args.workspace_root, args.version)
    output_path = protocol_manifest_path(args.workspace_root, args.output)
    write_json(output_path, manifest)
    print(json.dumps({
        "protocol_version": manifest["protocol_version"],
        "output_path": output_path.relative_to(args.workspace_root).as_posix(),
        "tracked_file_count": len(manifest.get("tracked_files", [])),
    }, indent=2, ensure_ascii=False))


def cmd_protocol_preflight(args: argparse.Namespace) -> None:
    manifest_path = protocol_manifest_path(args.workspace_root, args.manifest)
    summary = freeze_protocol_for_iteration(args.iteration, args.workspace_root, manifest_path)
    print(json.dumps(summary, indent=2, ensure_ascii=False))


def cmd_summarize_config(args: argparse.Namespace) -> None:
    skill_dir = args.skill_dir
    evals_path = args.evals
    metrics_path = args.metrics

    if skill_dir is None:
        if args.iteration is None or not args.skill or args.config is None:
            raise ValueError(
                "summarize-config requires --skill-dir, or legacy mode (--iteration, --skill, --config, [--workspace-root])"
            )
        skill_dir = args.iteration / args.skill

    if not skill_dir.exists():
        raise FileNotFoundError(f"Missing skill directory: {skill_dir}")

    if evals_path is None:
        if args.iteration is not None and args.skill:
            iteration_dir = args.iteration
            skill_name = args.skill
        else:
            iteration_dir = skill_dir.parent
            skill_name = skill_dir.name

        workspace_root = args.workspace_root
        if workspace_root is None:
            workspace_root = infer_workspace_root_from_iteration(iteration_dir)

        evals_path = resolve_public_evals_for_config(iteration_dir, workspace_root, skill_name, args.config)

    summary = summarize_config(skill_dir, args.config, evals_path, metrics_path)
    print(json.dumps({
        "skill_name": summary["skill_name"],
        "configuration": summary["configuration"],
        "eval_count": len(summary["evals"]),
        "output_json": str(skill_dir / f"{args.config}-summary.json"),
    }, indent=2, ensure_ascii=False))


def cmd_aggregate(args: argparse.Namespace) -> None:
    summary = aggregate_suite(args.iteration, args.workspace_root)
    write_json(args.iteration / "suite-summary.json", summary)
    write_text(args.iteration / "suite-summary.md", render_markdown(summary))
    print(json.dumps({
        "iteration": args.iteration.name,
        "skill_count": summary["skill_count"],
        "previous_iteration": summary["previous_iteration"],
        "metric_issue_count": summary.get("metric_validation", {}).get("issue_count", 0),
        "output_json": str(args.iteration / "suite-summary.json"),
        "output_md": str(args.iteration / "suite-summary.md"),
    }, indent=2, ensure_ascii=False))


def cmd_agent_plan(args: argparse.Namespace) -> None:
    plan = benchmark_agent_plan(args.iteration, args.skill, args.baseline_isolation)
    print(json.dumps(plan, indent=2, ensure_ascii=False))


def cmd_self_test(args: argparse.Namespace) -> None:
    summary = run_self_test(args.iteration, args.workspace_root, args.baseline_isolation)
    print(json.dumps(summary, indent=2, ensure_ascii=False))


def cmd_validate_blind_isolation(args: argparse.Namespace) -> None:
    summary = validate_blind_isolation(args.iteration)
    print(json.dumps(summary, indent=2, ensure_ascii=False))


def cmd_validate_executable_checks(args: argparse.Namespace) -> None:
    summary = validate_executable_checks(args.iteration, args.workspace_root)
    print(json.dumps(summary, indent=2, ensure_ascii=False))


def cmd_snapshot_public_evals(args: argparse.Namespace) -> None:
    summary = snapshot_public_evals(args.iteration, args.workspace_root, args.skill)
    print(json.dumps(summary, indent=2, ensure_ascii=False))


def cmd_blind_compare_bundle(args: argparse.Namespace) -> None:
    bundle = build_blind_compare_bundle(args.iteration, args.workspace_root, args.skill, args.eval_id, args.run_number)
    print(json.dumps(bundle, indent=2, ensure_ascii=False))


def cmd_export_review_workspace(args: argparse.Namespace) -> None:
    output_dir = args.output_dir or (args.iteration / args.skill / "_skill-creator-review-workspace")
    summary = export_review_workspace(args.iteration, args.workspace_root, args.skill, output_dir)
    print(json.dumps(summary, indent=2, ensure_ascii=False))


def cmd_analyzer_bundle(args: argparse.Namespace) -> None:
    bundle = build_benchmark_analysis_bundle(args.iteration, args.workspace_root, args.skill)
    print(json.dumps(bundle, indent=2, ensure_ascii=False))


def cmd_grader_bundle(args: argparse.Namespace) -> None:
    export_dir = args.export_dir or (args.iteration / args.skill / "_skill-creator-review-workspace")
    bundle = build_grader_bundle(
        args.iteration,
        args.workspace_root,
        args.skill,
        args.eval_id,
        args.configuration,
        export_dir,
    )
    print(json.dumps(bundle, indent=2, ensure_ascii=False))


def cmd_write_static_review(args: argparse.Namespace) -> None:
    output_html = args.output_html or (args.iteration / args.skill / "skill-creator-review.html")
    summary = write_static_review(args.iteration, args.workspace_root, args.skill, output_html)
    print(json.dumps(summary, indent=2, ensure_ascii=False))


def cmd_write_skill_creator_benchmark(args: argparse.Namespace) -> None:
    output_path = args.output or (args.iteration / args.skill / "skill-creator-benchmark.json")
    benchmark = write_skill_creator_benchmark(args.iteration, args.workspace_root, args.skill, output_path)
    print(json.dumps({
        "skill_name": args.skill,
        "output_json": str(output_path),
        "run_count": len(benchmark.get("runs", [])),
        "note_count": len(benchmark.get("notes", [])),
    }, indent=2, ensure_ascii=False))


def cmd_validate_metrics(args: argparse.Namespace) -> None:
    summary = validate_iteration_metrics(args.iteration)
    print(json.dumps(summary, indent=2, ensure_ascii=False))


def cmd_pre_aggregate_check(args: argparse.Namespace) -> None:
    summary = pre_aggregate_check(args.iteration, args.workspace_root)
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    if summary["status"] != "ok":
        raise SystemExit(1)


def cmd_resume_finalize(args: argparse.Namespace) -> None:
    summary = resume_finalize_iteration(
        args.iteration,
        args.workspace_root,
        materialize_from_meta=not args.no_materialize_from_meta,
    )
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    if summary["status"] != "ok":
        raise SystemExit(1)


def cmd_normalize_metrics(args: argparse.Namespace) -> None:
    summary = normalize_iteration_metrics(args.iteration)
    print(json.dumps(summary, indent=2, ensure_ascii=False))


def cmd_clean_benchmark_artifacts(args: argparse.Namespace) -> None:
    summary = clean_benchmark_artifacts(args.workspace_root)
    print(json.dumps(summary, indent=2, ensure_ascii=False))


def cmd_prune_generated_artifacts(args: argparse.Namespace) -> None:
    summary = prune_generated_artifacts(args.iteration, args.workspace_root)
    print(json.dumps(summary, indent=2, ensure_ascii=False))


def cmd_current_utc_timestamp(args: argparse.Namespace) -> None:
    print(json.dumps(current_utc_timestamp(), indent=2, ensure_ascii=False))


def cmd_write_run_metrics(args: argparse.Namespace) -> None:
    inferred = infer_run_metrics_fields(args.output)
    started_at = args.started_at
    finished_at = args.finished_at
    started_dt = iso_to_datetime(started_at)
    finished_dt = iso_to_datetime(finished_at)
    if not started_dt or not finished_dt:
        raise ValueError("started_at and finished_at must be valid ISO-8601 timestamps")

    elapsed_seconds_total = args.elapsed_seconds_total
    if elapsed_seconds_total is None:
        elapsed_seconds_total = round((finished_dt - started_dt).total_seconds(), 6)

    payload = build_run_metrics_payload(
        skill_name=args.skill_name or inferred.get("skill_name") or "unknown-skill",
        configuration=args.configuration or inferred.get("configuration") or "with_skill",
        language=args.language,
        mcp_used=args.mcp_used,
        started_at=started_at,
        finished_at=finished_at,
        elapsed_seconds_total=elapsed_seconds_total,
        files_read_count=args.files_read_count,
        files_written_count=args.files_written_count,
        run_number=args.run_number,
    )
    write_json(args.output, payload)
    print(json.dumps({
        "output": str(args.output),
        "skill_name": payload["skill_name"],
        "configuration": payload["configuration"],
        "elapsed_seconds_total": payload["elapsed_seconds_total"],
    }, indent=2, ensure_ascii=False))


def cmd_materialize_run(args: argparse.Namespace) -> None:
    summary = materialize_run_artifacts(
        args.iteration,
        args.skill,
        args.configuration,
        args.raw_json,
        run_number=args.run_number,
        started_at=args.started_at,
        finished_at=args.finished_at,
    )
    print(json.dumps(summary, indent=2, ensure_ascii=False))


def cmd_materialize_run_stdin(args: argparse.Namespace) -> None:
    raw_text = sys.stdin.read().strip()
    if not raw_text:
        raise ValueError("materialize-run-stdin requires a JSON payload on stdin")
    payload = json.loads(raw_text)
    raw_output = args.raw_json or (args.iteration / "_meta" / f"{args.skill}-{args.configuration}.json")
    write_json(raw_output, payload)
    summary = materialize_run_artifacts(
        args.iteration,
        args.skill,
        args.configuration,
        raw_output,
        run_number=args.run_number,
        started_at=args.started_at,
        finished_at=args.finished_at,
    )
    print(json.dumps(summary, indent=2, ensure_ascii=False))


def cmd_materialize_comparisons(args: argparse.Namespace) -> None:
    summary = materialize_blind_comparisons(args.iteration, args.skill, args.raw_json)
    workspace_root = infer_workspace_root_from_iteration(args.iteration)
    summary["suite_refresh"] = refresh_suite_outputs_after_blind(args.iteration, workspace_root, args.skill)
    print(json.dumps(summary, indent=2, ensure_ascii=False))


def cmd_materialize_comparisons_stdin(args: argparse.Namespace) -> None:
    raw_text = sys.stdin.read().strip()
    if not raw_text:
        raise ValueError("materialize-comparisons-stdin requires a JSON payload on stdin")
    payload = json.loads(raw_text)
    raw_output = args.raw_json or (args.iteration / "_meta" / f"{args.skill}-blind.json")
    write_json(raw_output, payload)
    summary = materialize_blind_comparisons(args.iteration, args.skill, raw_output)
    workspace_root = infer_workspace_root_from_iteration(args.iteration)
    summary["suite_refresh"] = refresh_suite_outputs_after_blind(args.iteration, workspace_root, args.skill)
    print(json.dumps(summary, indent=2, ensure_ascii=False))


def completed_skill_names_for_config(iteration_dir: Path, config: str) -> list[str]:
    result: list[str] = []
    for skill_dir in skill_dirs(iteration_dir):
        if (skill_dir / f"{config}-run-metrics.json").exists():
            result.append(skill_dir.name)
    return sorted(result)


def infer_workspace_root_from_iteration(iteration_dir: Path) -> Path:
    resolved = iteration_dir.resolve()
    if resolved.parent.name == "test":
        return resolved.parent.parent
    return resolved.parent.parent


def resolve_public_evals_for_config(iteration_dir: Path, workspace_root: Path, skill_name: str, config: str) -> Path:
    workspace_path = skill_eval_paths(workspace_root, skill_name)["public"]
    disabled_path = disabled_skills_root(iteration_dir) / skill_name / "evals" / EVALS_PUBLIC_FILENAME
    candidates = [workspace_path, disabled_path] if config == "with_skill" else [disabled_path, workspace_path]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    raise FileNotFoundError(f"Missing {EVALS_PUBLIC_FILENAME} for skill '{skill_name}' while summarizing {config}")


def refresh_suite_outputs_after_blind(
    iteration_dir: Path,
    workspace_root: Path,
    skill_name: str | None = None,
) -> dict[str, Any]:
    skills = [skill_name] if skill_name else [path.name for path in skill_dirs(iteration_dir)]
    summarized: list[dict[str, Any]] = []

    for name in skills:
        skill_dir = iteration_dir / name
        if not skill_dir.exists():
            continue
        for config in ("with_skill", "without_skill"):
            metrics_path = skill_dir / f"{config}-run-metrics.json"
            if not metrics_path.exists():
                continue
            evals_path = resolve_public_evals_for_config(iteration_dir, workspace_root, name, config)
            summary = summarize_config(skill_dir, config, evals_path)
            summarized.append(
                {
                    "skill": name,
                    "configuration": config,
                    "eval_count": len(summary.get("evals", [])),
                    "run_count": summary.get("run_count", 1),
                    "summary_path": (skill_dir / f"{config}-summary.json").relative_to(workspace_root).as_posix(),
                }
            )

    suite_summary = aggregate_suite(iteration_dir, workspace_root)
    suite_summary_json = iteration_dir / "suite-summary.json"
    suite_summary_md = iteration_dir / "suite-summary.md"
    write_json(suite_summary_json, suite_summary)
    write_text(suite_summary_md, render_markdown(suite_summary))

    return {
        "iteration": iteration_dir.name,
        "summarized_count": len(summarized),
        "summarized": summarized,
        "suite_summary_json": suite_summary_json.relative_to(workspace_root).as_posix(),
        "suite_summary_md": suite_summary_md.relative_to(workspace_root).as_posix(),
        "skill_count": suite_summary.get("skill_count", 0),
    }


def resume_finalize_iteration(
    iteration_dir: Path,
    workspace_root: Path,
    *,
    materialize_from_meta: bool = True,
) -> dict[str, Any]:
    meta_dir = iteration_dir / "_meta"
    materialized: list[dict[str, Any]] = []
    unresolved: list[dict[str, Any]] = []

    for skill_dir in skill_dirs(iteration_dir):
        comparisons_path = skill_dir / "blind-comparisons.json"
        if comparisons_path.exists():
            continue

        raw_path = meta_dir / f"{skill_dir.name}-blind.json"
        if materialize_from_meta and raw_path.exists():
            materialized_summary = materialize_blind_comparisons(iteration_dir, skill_dir.name, raw_path)
            materialized.append(
                {
                    "skill": skill_dir.name,
                    "raw_json": raw_path.relative_to(workspace_root).as_posix(),
                    "comparison_count": materialized_summary.get("comparison_count", 0),
                    "output_path": comparisons_path.relative_to(workspace_root).as_posix(),
                }
            )
            continue

        unresolved.append(
            {
                "skill": skill_dir.name,
                "reason": "missing blind-comparisons and no resumable raw comparator payload",
                "expected_raw_payload": raw_path.relative_to(workspace_root).as_posix(),
            }
        )

    precheck = pre_aggregate_check(iteration_dir, workspace_root)
    if precheck.get("status") != "ok":
        return {
            "iteration": iteration_dir.name,
            "status": "blocked",
            "materialize_from_meta": materialize_from_meta,
            "materialized_count": len(materialized),
            "materialized": materialized,
            "unresolved_count": len(unresolved),
            "unresolved": unresolved,
            "pre_aggregate_check": precheck,
            "aggregate": None,
        }

    aggregate_summary = aggregate_suite(iteration_dir, workspace_root)
    write_json(iteration_dir / "suite-summary.json", aggregate_summary)
    write_text(iteration_dir / "suite-summary.md", render_markdown(aggregate_summary))

    return {
        "iteration": iteration_dir.name,
        "status": "ok",
        "materialize_from_meta": materialize_from_meta,
        "materialized_count": len(materialized),
        "materialized": materialized,
        "unresolved_count": len(unresolved),
        "unresolved": unresolved,
        "pre_aggregate_check": precheck,
        "aggregate": {
            "skill_count": aggregate_summary.get("skill_count", 0),
            "metric_issue_count": aggregate_summary.get("metric_validation", {}).get("issue_count", 0),
            "output_json": (iteration_dir / "suite-summary.json").relative_to(workspace_root).as_posix(),
            "output_md": (iteration_dir / "suite-summary.md").relative_to(workspace_root).as_posix(),
        },
    }


def cmd_summarize_phase(args: argparse.Namespace) -> None:
    skill_names = [args.skill] if args.skill else completed_skill_names_for_config(args.iteration, args.config)
    summaries = []
    for skill_name in skill_names:
        skill_dir = args.iteration / skill_name
        evals_path = resolve_public_evals_for_config(args.iteration, args.workspace_root, skill_name, args.config)
        summary = summarize_config(skill_dir, args.config, evals_path)
        summaries.append(
            {
                "skill_name": skill_name,
                "configuration": args.config,
                "eval_count": len(summary.get("evals", [])),
                "run_count": summary.get("run_count", 1),
                "output_json": (skill_dir / f"{args.config}-summary.json").relative_to(args.workspace_root).as_posix(),
            }
        )
    print(json.dumps({
        "iteration": args.iteration.name,
        "configuration": args.config,
        "skill_count": len(summaries),
        "skills": summaries,
    }, indent=2, ensure_ascii=False))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Utility helpers for the skill evaluation suite")
    subparsers = parser.add_subparsers(dest="command", required=True)

    reset_debug_log_parser = subparsers.add_parser("reset-debug-log", help="Create or clear a hook debug JSONL log file")
    reset_debug_log_parser.add_argument("--path", type=Path, required=True, help="Path to the debug log file")
    reset_debug_log_parser.set_defaults(func=cmd_reset_debug_log)

    debug_log_window_parser = subparsers.add_parser("debug-log-window", help="Report the first and last timestamps captured in a hook debug JSONL log")
    debug_log_window_parser.add_argument("--path", type=Path, required=True, help="Path to the debug log file")
    debug_log_window_parser.set_defaults(func=cmd_debug_log_window)

    validate_hook_audit_parser = subparsers.add_parser("validate-hook-audit", help="Validate resolved hook-audit decisions for benchmark worker modes")
    validate_hook_audit_parser.add_argument("--path", type=Path, default=HOOK_AUDIT_LOG_RELATIVE_PATH, help=f"Path to the hook-audit JSONL file (default: {HOOK_AUDIT_LOG_RELATIVE_PATH.as_posix()})")
    validate_hook_audit_parser.add_argument("--mode", choices=["benchmark_manager", "baseline", "baseline_hook_only", "with_skill_targeted", "blind_compare"], help="Optional benchmark mode filter")
    validate_hook_audit_parser.set_defaults(func=cmd_validate_hook_audit)

    reset_hook_state_parser = subparsers.add_parser("reset-hook-state", help="Remove persisted benchmark hook session state before starting a fresh worker")
    reset_hook_state_parser.add_argument("--workspace-root", type=Path, required=True, help="Workspace root path")
    reset_hook_state_group = reset_hook_state_parser.add_mutually_exclusive_group(required=True)
    reset_hook_state_group.add_argument("--mode", choices=BENCH_HOOK_MODES, help="Benchmark hook mode whose anonymous session state should be cleared")
    reset_hook_state_group.add_argument("--session-id", help="Explicit hook session id to clear")
    reset_hook_state_parser.set_defaults(func=cmd_reset_hook_state)

    protocol_manifest_parser = subparsers.add_parser("write-protocol-manifest", help="Write the benchmark protocol manifest with hashes for tracked prompts, schemas, and hooks")
    protocol_manifest_parser.add_argument("--workspace-root", type=Path, required=True, help="Workspace root path")
    protocol_manifest_parser.add_argument("--output", type=Path, help="Optional output path for the manifest JSON")
    protocol_manifest_parser.add_argument("--version", default=BENCHMARK_PROTOCOL_VERSION, help=f"Protocol version label (default: {BENCHMARK_PROTOCOL_VERSION})")
    protocol_manifest_parser.set_defaults(func=cmd_write_protocol_manifest)

    protocol_preflight_parser = subparsers.add_parser("protocol-preflight", help="Validate the frozen protocol manifest and lock the current protocol version into an iteration")
    protocol_preflight_parser.add_argument("--iteration", type=Path, required=True, help="Path to /test/iteration-N")
    protocol_preflight_parser.add_argument("--workspace-root", type=Path, required=True, help="Workspace root path")
    protocol_preflight_parser.add_argument("--manifest", type=Path, help="Optional path to the benchmark protocol manifest JSON")
    protocol_preflight_parser.set_defaults(func=cmd_protocol_preflight)

    disable_parser = subparsers.add_parser("disable-workspace-skills", help="Move workspace skills out of .github/skills for baseline runs")
    disable_parser.add_argument("--workspace-root", type=Path, required=True, help="Workspace root path")
    disable_parser.add_argument("--iteration", type=Path, required=True, help="Path to /test/iteration-N")
    disable_parser.set_defaults(func=cmd_disable_workspace_skills)

    restore_parser = subparsers.add_parser("restore-workspace-skills", help="Restore workspace skills back into .github/skills after baseline runs")
    restore_parser.add_argument("--workspace-root", type=Path, required=True, help="Workspace root path")
    restore_parser.add_argument("--iteration", type=Path, required=True, help="Path to /test/iteration-N")
    restore_parser.set_defaults(func=cmd_restore_workspace_skills)

    prepare_parser = subparsers.add_parser("prepare-blind", help="Create blinded A/B artifacts for each finished eval")
    prepare_parser.add_argument("--iteration", type=Path, required=True, help="Path to /test/iteration-N")
    prepare_parser.set_defaults(func=cmd_prepare_blind)

    summarize_parser = subparsers.add_parser("summarize-config", help="Build a per-skill per-configuration summary JSON")
    summarize_parser.add_argument("--skill-dir", type=Path, help="Path to /test/iteration-N/<skill-name>")
    summarize_parser.add_argument("--config", choices=["with_skill", "without_skill"], required=True, help="Configuration name")
    summarize_parser.add_argument("--evals", type=Path, help="Path to the skill evals-public.json file")
    summarize_parser.add_argument("--metrics", type=Path, help="Optional path to the run-metrics JSON file")
    summarize_parser.add_argument("--iteration", type=Path, help="Legacy mode: path to /test/iteration-N")
    summarize_parser.add_argument("--skill", help="Legacy mode: target skill name")
    summarize_parser.add_argument("--workspace-root", type=Path, help="Legacy mode: workspace root path (auto-inferred when omitted)")
    summarize_parser.set_defaults(func=cmd_summarize_config)

    summarize_phase_parser = subparsers.add_parser("summarize-phase", help="Write per-skill summary JSON files for every completed skill in one benchmark phase")
    summarize_phase_parser.add_argument("--iteration", type=Path, required=True, help="Path to /test/iteration-N")
    summarize_phase_parser.add_argument("--workspace-root", type=Path, required=True, help="Workspace root path")
    summarize_phase_parser.add_argument("--config", choices=["with_skill", "without_skill"], required=True, help="Configuration name")
    summarize_phase_parser.add_argument("--skill", help="Optional single skill to summarize")
    summarize_phase_parser.set_defaults(func=cmd_summarize_phase)

    write_metrics_parser = subparsers.add_parser("write-run-metrics", help="Write a canonical run-metrics JSON file using the required benchmark schema")
    write_metrics_parser.add_argument("--output", type=Path, required=True, help="Path to the target *-run-metrics.json file")
    write_metrics_parser.add_argument("--skill-name", help="Optional skill name; inferred from the output path when omitted")
    write_metrics_parser.add_argument("--configuration", choices=["with_skill", "without_skill"], help="Optional configuration; inferred from the output filename when omitted")
    write_metrics_parser.add_argument("--language", default="English", help="Language used for the run output (default: English)")
    write_metrics_parser.add_argument("--mcp-used", action="store_true", help="Set this flag if any MCP tool was used during the run")
    write_metrics_parser.add_argument("--started-at", required=True, help="ISO-8601 UTC timestamp for run start")
    write_metrics_parser.add_argument("--finished-at", required=True, help="ISO-8601 UTC timestamp for run finish")
    write_metrics_parser.add_argument("--elapsed-seconds-total", type=float, help="Optional explicit elapsed time; otherwise derived from timestamps")
    write_metrics_parser.add_argument("--files-read-count", type=int, required=True, help="Repository files intentionally read during the run")
    write_metrics_parser.add_argument("--files-written-count", type=int, required=True, help="Files written under /test during the run")
    write_metrics_parser.add_argument("--run-number", type=int, default=1, help="Repeated-run index for this metrics payload (default: 1)")
    write_metrics_parser.set_defaults(func=cmd_write_run_metrics)

    materialize_run_parser = subparsers.add_parser(
        "materialize-run",
        help="Write response.md files and canonical run-metrics.json from one raw benchmark worker JSON payload",
    )
    materialize_run_parser.add_argument("--iteration", type=Path, required=True, help="Path to /test/iteration-N")
    materialize_run_parser.add_argument("--skill", required=True, help="Target skill name")
    materialize_run_parser.add_argument("--configuration", choices=["with_skill", "without_skill"], required=True, help="Configuration name")
    materialize_run_parser.add_argument("--raw-json", type=Path, required=True, help="Path to the raw worker JSON payload")
    materialize_run_parser.add_argument("--run-number", type=int, default=1, help="Repeated-run index for this worker payload (default: 1)")
    materialize_run_parser.add_argument("--started-at", help="Optional ISO-8601 UTC timestamp to override the raw payload start time")
    materialize_run_parser.add_argument("--finished-at", help="Optional ISO-8601 UTC timestamp to override the raw payload finish time")
    materialize_run_parser.set_defaults(func=cmd_materialize_run)

    materialize_run_stdin_parser = subparsers.add_parser(
        "materialize-run-stdin",
        help="Read one raw benchmark worker JSON payload from stdin, persist it under test/iteration-N/_meta, and materialize run artifacts",
    )
    materialize_run_stdin_parser.add_argument("--iteration", type=Path, required=True, help="Path to /test/iteration-N")
    materialize_run_stdin_parser.add_argument("--skill", required=True, help="Target skill name")
    materialize_run_stdin_parser.add_argument("--configuration", choices=["with_skill", "without_skill"], required=True, help="Configuration name")
    materialize_run_stdin_parser.add_argument("--raw-json", type=Path, help="Optional output path for the persisted raw JSON payload")
    materialize_run_stdin_parser.add_argument("--run-number", type=int, default=1, help="Repeated-run index for this worker payload (default: 1)")
    materialize_run_stdin_parser.add_argument("--started-at", help="Optional ISO-8601 UTC timestamp to override the raw payload start time")
    materialize_run_stdin_parser.add_argument("--finished-at", help="Optional ISO-8601 UTC timestamp to override the raw payload finish time")
    materialize_run_stdin_parser.set_defaults(func=cmd_materialize_run_stdin)

    materialize_comparisons_parser = subparsers.add_parser(
        "materialize-comparisons",
        help="Write blind-comparisons.json from one raw comparator JSON payload",
    )
    materialize_comparisons_parser.add_argument("--iteration", type=Path, required=True, help="Path to /test/iteration-N")
    materialize_comparisons_parser.add_argument("--skill", required=True, help="Target skill name")
    materialize_comparisons_parser.add_argument("--raw-json", type=Path, required=True, help="Path to the raw comparator JSON payload")
    materialize_comparisons_parser.set_defaults(func=cmd_materialize_comparisons)

    materialize_comparisons_stdin_parser = subparsers.add_parser(
        "materialize-comparisons-stdin",
        help="Read one raw blind comparator JSON payload from stdin, persist it under test/iteration-N/_meta, and materialize blind-comparisons.json",
    )
    materialize_comparisons_stdin_parser.add_argument("--iteration", type=Path, required=True, help="Path to /test/iteration-N")
    materialize_comparisons_stdin_parser.add_argument("--skill", required=True, help="Target skill name")
    materialize_comparisons_stdin_parser.add_argument("--raw-json", type=Path, help="Optional output path for the persisted raw comparator JSON payload")
    materialize_comparisons_stdin_parser.set_defaults(func=cmd_materialize_comparisons_stdin)

    validate_parser = subparsers.add_parser("validate-metrics", help="Validate that every run-metrics file exists and contains all required non-null keys")
    validate_parser.add_argument("--iteration", type=Path, required=True, help="Path to /test/iteration-N")
    validate_parser.set_defaults(func=cmd_validate_metrics)

    pre_aggregate_parser = subparsers.add_parser("pre-aggregate-check", help="Fail-fast readiness check before final aggregation")
    pre_aggregate_parser.add_argument("--iteration", type=Path, required=True, help="Path to /test/iteration-N")
    pre_aggregate_parser.add_argument("--workspace-root", type=Path, required=True, help="Workspace root path")
    pre_aggregate_parser.set_defaults(func=cmd_pre_aggregate_check)

    resume_finalize_parser = subparsers.add_parser(
        "resume-finalize",
        help="Resume-safe finalization: materialize missing blind-comparisons from _meta payloads, run pre-aggregate-check, then aggregate",
    )
    resume_finalize_parser.add_argument("--iteration", type=Path, required=True, help="Path to /test/iteration-N")
    resume_finalize_parser.add_argument("--workspace-root", type=Path, required=True, help="Workspace root path")
    resume_finalize_parser.add_argument(
        "--no-materialize-from-meta",
        action="store_true",
        help="Disable auto-materialization from test/<iteration>/_meta/<skill>-blind.json",
    )
    resume_finalize_parser.set_defaults(func=cmd_resume_finalize)

    normalize_parser = subparsers.add_parser("normalize-metrics", help="Normalize known legacy run-metrics aliases into the canonical benchmark schema")
    normalize_parser.add_argument("--iteration", type=Path, required=True, help="Path to /test/iteration-N")
    normalize_parser.set_defaults(func=cmd_normalize_metrics)

    clean_parser = subparsers.add_parser("clean-benchmark-artifacts", help="Remove generated benchmark iteration directories and disposable benchmark artefacts")
    clean_parser.add_argument("--workspace-root", type=Path, required=True, help="Workspace root path")
    clean_parser.set_defaults(func=cmd_clean_benchmark_artifacts)

    prune_parser = subparsers.add_parser("prune-generated-artifacts", help="Remove disposable per-iteration exports that are not part of the canonical benchmark outputs")
    prune_parser.add_argument("--iteration", type=Path, required=True, help="Path to /test/iteration-N or /test/<series>-testN")
    prune_parser.add_argument("--workspace-root", type=Path, required=True, help="Workspace root path")
    prune_parser.set_defaults(func=cmd_prune_generated_artifacts)

    utc_now_parser = subparsers.add_parser("utc-now", help="Print the current UTC timestamp in benchmark-friendly ISO-8601 format")
    utc_now_parser.set_defaults(func=cmd_current_utc_timestamp)

    aggregate_parser = subparsers.add_parser("aggregate", help="Aggregate per-skill results into suite-summary files")
    aggregate_parser.add_argument("--iteration", type=Path, required=True, help="Path to /test/iteration-N")
    aggregate_parser.add_argument("--workspace-root", type=Path, required=True, help="Workspace root path")
    aggregate_parser.set_defaults(func=cmd_aggregate)

    agent_plan_parser = subparsers.add_parser("agent-plan", help="Describe which benchmark custom agent should be used for each benchmark phase")
    agent_plan_parser.add_argument("--iteration", type=Path, required=True, help="Path to /test/iteration-N")
    agent_plan_parser.add_argument("--skill", help="Optional target skill name for with_skill planning")
    agent_plan_parser.add_argument("--baseline-isolation", choices=["relocation", "hook-only"], default="relocation", help="Baseline isolation strategy to plan for (default: relocation)")
    agent_plan_parser.set_defaults(func=cmd_agent_plan)

    self_test_parser = subparsers.add_parser("self-test", help="Run the benchmark stack offline checks from a single automation entrypoint")
    self_test_parser.add_argument("--iteration", type=Path, required=True, help="Path to /test/iteration-N")
    self_test_parser.add_argument("--workspace-root", type=Path, required=True, help="Workspace root path")
    self_test_parser.add_argument("--baseline-isolation", choices=["relocation", "hook-only"], default="relocation", help="Baseline isolation strategy to sanity-check (default: relocation)")
    self_test_parser.set_defaults(func=cmd_self_test)

    validate_blind_parser = subparsers.add_parser("validate-blind-isolation", help="Validate that blind artifacts stayed isolated from mapping and non-blind references")
    validate_blind_parser.add_argument("--iteration", type=Path, required=True, help="Path to /test/iteration-N")
    validate_blind_parser.set_defaults(func=cmd_validate_blind_isolation)

    executable_parser = subparsers.add_parser("validate-executable-checks", help="Run automated LikeC4 snippet validation across benchmark responses")
    executable_parser.add_argument("--iteration", type=Path, required=True, help="Path to /test/iteration-N")
    executable_parser.add_argument("--workspace-root", type=Path, required=True, help="Workspace root path")
    executable_parser.set_defaults(func=cmd_validate_executable_checks)

    snapshot_public_parser = subparsers.add_parser("snapshot-public-evals", help="Copy the current evals-public prompts into the iteration meta folder before strict baseline runs")
    snapshot_public_parser.add_argument("--iteration", type=Path, required=True, help="Path to /test/iteration-N")
    snapshot_public_parser.add_argument("--workspace-root", type=Path, required=True, help="Workspace root path")
    snapshot_public_parser.add_argument("--skill", help="Optional single skill to snapshot")
    snapshot_public_parser.set_defaults(func=cmd_snapshot_public_evals)

    blind_bundle_parser = subparsers.add_parser("blind-compare-bundle", help="Build the blind-comparison input bundle for one skill eval using the benchmark comparator playbook")
    blind_bundle_parser.add_argument("--iteration", type=Path, required=True, help="Path to /test/iteration-N")
    blind_bundle_parser.add_argument("--workspace-root", type=Path, required=True, help="Workspace root path")
    blind_bundle_parser.add_argument("--skill", required=True, help="Target skill name")
    blind_bundle_parser.add_argument("--eval-id", type=int, required=True, help="Eval id inside the split eval artifacts")
    blind_bundle_parser.add_argument("--run-number", type=int, default=1, help="Repeated-run index to bundle for blind comparison (default: 1)")
    blind_bundle_parser.set_defaults(func=cmd_blind_compare_bundle)

    export_review_parser = subparsers.add_parser("export-review-workspace", help="Export one skill iteration into a skill-creator-compatible review workspace layout")
    export_review_parser.add_argument("--iteration", type=Path, required=True, help="Path to /test/iteration-N")
    export_review_parser.add_argument("--workspace-root", type=Path, required=True, help="Workspace root path")
    export_review_parser.add_argument("--skill", required=True, help="Target skill name")
    export_review_parser.add_argument("--output-dir", type=Path, help="Optional output directory for the exported review workspace")
    export_review_parser.set_defaults(func=cmd_export_review_workspace)

    analyzer_bundle_parser = subparsers.add_parser("analyzer-bundle", help="Build the benchmark-analysis input bundle aligned with skill-creator/agents/analyzer.md")
    analyzer_bundle_parser.add_argument("--iteration", type=Path, required=True, help="Path to /test/iteration-N")
    analyzer_bundle_parser.add_argument("--workspace-root", type=Path, required=True, help="Workspace root path")
    analyzer_bundle_parser.add_argument("--skill", required=True, help="Target skill name")
    analyzer_bundle_parser.set_defaults(func=cmd_analyzer_bundle)

    grader_bundle_parser = subparsers.add_parser("grader-bundle", help="Build the grading input bundle aligned with skill-creator/agents/grader.md for one exported benchmark run")
    grader_bundle_parser.add_argument("--iteration", type=Path, required=True, help="Path to /test/iteration-N")
    grader_bundle_parser.add_argument("--workspace-root", type=Path, required=True, help="Workspace root path")
    grader_bundle_parser.add_argument("--skill", required=True, help="Target skill name")
    grader_bundle_parser.add_argument("--eval-id", type=int, required=True, help="Eval id inside the split eval artifacts")
    grader_bundle_parser.add_argument("--configuration", choices=["with_skill", "without_skill"], required=True, help="Configuration to grade")
    grader_bundle_parser.add_argument("--export-dir", type=Path, help="Optional exported review workspace directory")
    grader_bundle_parser.set_defaults(func=cmd_grader_bundle)

    static_review_parser = subparsers.add_parser("write-static-review", help="Generate a static HTML review by adapting the current iteration to skill-creator's eval viewer")
    static_review_parser.add_argument("--iteration", type=Path, required=True, help="Path to /test/iteration-N")
    static_review_parser.add_argument("--workspace-root", type=Path, required=True, help="Workspace root path")
    static_review_parser.add_argument("--skill", required=True, help="Target skill name")
    static_review_parser.add_argument("--output-html", type=Path, help="Optional path for the generated static HTML review")
    static_review_parser.set_defaults(func=cmd_write_static_review)

    benchmark_export_parser = subparsers.add_parser("write-skill-creator-benchmark", help="Write a skill-creator-compatible benchmark.json export for one benchmarked skill")
    benchmark_export_parser.add_argument("--iteration", type=Path, required=True, help="Path to /test/iteration-N")
    benchmark_export_parser.add_argument("--workspace-root", type=Path, required=True, help="Workspace root path")
    benchmark_export_parser.add_argument("--skill", required=True, help="Target skill name")
    benchmark_export_parser.add_argument("--output", type=Path, help="Optional output path for the generated benchmark JSON")
    benchmark_export_parser.set_defaults(func=cmd_write_skill_creator_benchmark)

    synthesis_bundle_parser = subparsers.add_parser("synthesis-bundle", help="Build the complete data bundle for generating a critical synthesis report for one benchmarked skill")
    synthesis_bundle_parser.add_argument("--iteration", type=Path, required=True, help="Path to /test/iteration-N")
    synthesis_bundle_parser.add_argument("--workspace-root", type=Path, required=True, help="Workspace root path")
    synthesis_bundle_parser.add_argument("--skill", required=True, help="Target skill name")
    synthesis_bundle_parser.set_defaults(func=cmd_synthesis_bundle)

    write_synthesis_parser = subparsers.add_parser("write-synthesis", help="Write a critical synthesis markdown report for one benchmarked skill")
    write_synthesis_parser.add_argument("--iteration", type=Path, required=True, help="Path to /test/iteration-N")
    write_synthesis_parser.add_argument("--workspace-root", type=Path, required=True, help="Workspace root path")
    write_synthesis_parser.add_argument("--skill", required=True, help="Target skill name")
    write_synthesis_parser.add_argument("--content-file", type=Path, help="Path to a markdown file with the synthesis content (if omitted, reads from stdin)")
    write_synthesis_parser.add_argument("--output", type=Path, help="Optional output path for the synthesis markdown")
    write_synthesis_parser.set_defaults(func=cmd_write_synthesis)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    if hasattr(args, "iteration") and isinstance(args.iteration, Path):
        args.iteration = args.iteration.resolve()
    if hasattr(args, "workspace_root") and isinstance(args.workspace_root, Path):
        args.workspace_root = args.workspace_root.resolve()
    args.func(args)


if __name__ == "__main__":
    main()
