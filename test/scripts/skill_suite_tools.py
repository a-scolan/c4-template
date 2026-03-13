from __future__ import annotations

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
from statistics import mean
from typing import Any


ITERATION_RE = re.compile(r"^iteration-(\d+)$")
WORD_RE = re.compile(r"\S+")

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


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def extract_timestamp_field(payload: dict[str, Any], *keys: str) -> str | None:
    for key in keys:
        value = payload.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return None


def extract_files_read_count(payload: dict[str, Any]) -> int:
    files_read = payload.get("files_read")
    if isinstance(files_read, list):
        normalized = [str(item).strip() for item in files_read if str(item).strip()]
        seen: set[str] = set()
        for item in normalized:
            seen.add(item)
        return len(seen)
    explicit_count = coerce_int(payload.get("files_read_count"))
    return explicit_count if explicit_count is not None else 0


def materialize_run_artifacts(
    iteration_dir: Path,
    skill_name: str,
    configuration: str,
    raw_json_path: Path,
    *,
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

        output_path = skill_dir / f"eval-{eval_id}" / configuration / "response.md"
        write_text(output_path, response.rstrip() + "\n")
        written_files.append(output_path.relative_to(iteration_dir).as_posix())

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
    )
    write_json(skill_dir / f"{configuration}-run-metrics.json", metrics_payload)

    return {
        "iteration": iteration_dir.name,
        "skill_name": skill_name,
        "configuration": configuration,
        "raw_json": str(raw_json_path),
        "responses_written": len(written_files),
        "written_files": written_files,
        "run_metrics_path": str(skill_dir / f"{configuration}-run-metrics.json"),
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

    output_path = iteration_dir / skill_name / "blind-comparisons.json"
    write_json(
        output_path,
        {
            "skill_name": skill_name,
            "comparisons": comparisons,
        },
    )
    return {
        "iteration": iteration_dir.name,
        "skill_name": skill_name,
        "raw_json": str(raw_json_path),
        "comparison_count": len(comparisons),
        "output_path": str(output_path),
    }


def count_words(text: str) -> int:
    return len(WORD_RE.findall(text))


def safe_mean(values: list[float]) -> float | None:
    cleaned = [value for value in values if value is not None]
    if not cleaned:
        return None
    return round(mean(cleaned), 4)


def round_or_none(value: float | None, digits: int = 4) -> float | None:
    if value is None:
        return None
    return round(value, digits)


def iso_to_datetime(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value.strip():
        return None
    normalized = value.strip()
    if normalized.endswith("Z"):
        normalized = normalized[:-1] + "+00:00"
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def coerce_bool(value: Any) -> bool | None:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        lowered = value.strip().lower()
        if lowered in {"true", "1", "yes", "y"}:
            return True
        if lowered in {"false", "0", "no", "n"}:
            return False
    return None


def coerce_int(value: Any) -> int | None:
    if value is None or isinstance(value, bool):
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def coerce_float(value: Any) -> float | None:
    if value is None or isinstance(value, bool):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def infer_run_metrics_fields(metrics_path: Path) -> dict[str, str | None]:
    configuration = None
    file_name = metrics_path.name
    for candidate in ("with_skill", "without_skill"):
        if file_name == f"{candidate}-run-metrics.json":
            configuration = candidate
            break
    return {
        "skill_name": metrics_path.parent.name if metrics_path.parent != metrics_path else None,
        "configuration": configuration,
    }


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
) -> dict[str, Any]:
    return {
        "skill_name": skill_name,
        "configuration": configuration,
        "language": language,
        "mcp_used": mcp_used,
        "started_at": started_at,
        "finished_at": finished_at,
        "elapsed_seconds_total": elapsed_seconds_total,
        "files_read_count": files_read_count,
        "files_written_count": files_written_count,
    }


def canonicalize_run_metrics(metrics: dict[str, Any], metrics_path: Path | None = None) -> tuple[dict[str, Any], list[str]]:
    inferred = infer_run_metrics_fields(metrics_path) if metrics_path else {}
    canonical: dict[str, Any] = {}
    changes: list[str] = []

    for key in REQUIRED_RUN_METRIC_KEYS:
        aliases = RUN_METRIC_KEY_ALIASES.get(key, (key,))
        value = None
        source_key = None
        for alias in aliases:
            if alias in metrics and metrics[alias] is not None:
                value = metrics[alias]
                source_key = alias
                break

        if value is None and key in RUN_METRIC_LIST_FALLBACKS:
            for list_key in RUN_METRIC_LIST_FALLBACKS[key]:
                list_value = metrics.get(list_key)
                if isinstance(list_value, list):
                    value = len(list_value)
                    source_key = list_key
                    changes.append(f"derived {key} from {list_key}")
                    break

        if value is None and inferred.get(key) is not None:
            value = inferred[key]
            changes.append(f"inferred {key} from metrics path")

        if value is None and key in RUN_METRIC_DEFAULTS:
            value = RUN_METRIC_DEFAULTS[key]
            changes.append(f"defaulted {key}")

        if key == "mcp_used":
            coerced = coerce_bool(value)
            if value is not None and coerced is None:
                changes.append(f"could not coerce {key}; leaving as-is")
            value = coerced if coerced is not None else value
        elif key in {"files_read_count", "files_written_count"}:
            coerced = coerce_int(value)
            value = coerced if coerced is not None else value
        elif key == "elapsed_seconds_total":
            coerced = coerce_float(value)
            value = coerced if coerced is not None else value

        if source_key and source_key != key:
            changes.append(f"mapped {source_key} -> {key}")

        canonical[key] = value

    if canonical.get("elapsed_seconds_total") is None:
        started_at = iso_to_datetime(canonical.get("started_at"))
        finished_at = iso_to_datetime(canonical.get("finished_at"))
        if started_at and finished_at:
            canonical["elapsed_seconds_total"] = round((finished_at - started_at).total_seconds(), 6)
            changes.append("derived elapsed_seconds_total from started_at and finished_at")

    normalized = {key: canonical.get(key) for key in REQUIRED_RUN_METRIC_KEYS}
    for key, value in metrics.items():
        if key in normalized or key in RUN_METRIC_ALIAS_KEYS_TO_DROP:
            continue
        normalized[key] = value

    return normalized, changes


def load_run_metrics(metrics_path: Path, *, write_back: bool) -> tuple[dict[str, Any], list[str]]:
    metrics = read_json(metrics_path)
    normalized, changes = canonicalize_run_metrics(metrics, metrics_path)
    if write_back and (changes or normalized != metrics):
        write_json(metrics_path, normalized)
    return normalized, changes


def delta_or_none(left: float | int | None, right: float | int | None, digits: int = 4) -> float | None:
    if left is None or right is None:
        return None
    return round(float(left) - float(right), digits)


def iteration_number(path: Path) -> int | None:
    match = ITERATION_RE.match(path.name)
    return int(match.group(1)) if match else None


def relative_to_root(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


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
    current_number = iteration_number(current_iteration)
    candidates: list[tuple[int, Path]] = []
    for child in test_root.iterdir():
        if not child.is_dir():
            continue
        number = iteration_number(child)
        if number is None:
            continue
        if current_number is not None and number < current_number:
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


def load_skill_eval_definition(workspace_root: Path, skill_name: str) -> dict[str, Any]:
    evals_path = workspace_root / ".github" / "skills" / skill_name / "evals" / "evals.json"
    if not evals_path.exists():
        raise FileNotFoundError(f"Missing eval definition for skill '{skill_name}': {evals_path}")
    return read_json(evals_path)


def get_eval_entry(eval_definition: dict[str, Any], eval_id: int) -> dict[str, Any]:
    for item in eval_definition.get("evals", []):
        if item.get("id") == eval_id:
            return item
    raise KeyError(f"No eval with id={eval_id}")


def build_blind_compare_bundle(iteration_dir: Path, workspace_root: Path, skill_name: str, eval_id: int) -> dict[str, Any]:
    eval_dir = iteration_dir / skill_name / f"eval-{eval_id}"
    blind_dir = eval_dir / "blind"
    a_path = blind_dir / "A.md"
    b_path = blind_dir / "B.md"
    eval_definition = load_skill_eval_definition(workspace_root, skill_name)
    eval_entry = get_eval_entry(eval_definition, eval_id)

    if not a_path.exists() or not b_path.exists():
        raise FileNotFoundError(
            f"Missing blind artifacts for {skill_name} eval-{eval_id}: expected {a_path} and {b_path}"
        )

    return {
        "iteration": iteration_dir.name,
        "skill_name": skill_name,
        "eval_id": eval_id,
        "blind_artifacts": {
            "A": a_path.relative_to(workspace_root).as_posix(),
            "B": b_path.relative_to(workspace_root).as_posix(),
        },
        "eval_prompt": eval_entry.get("prompt"),
        "expected_output": eval_entry.get("expected_output"),
        "expectations": eval_entry.get("expectations", []),
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
            "winner": "A | B | TIE",
            "reasoning": "string",
            "rubric": {
                "A": {"overall_score": "number"},
                "B": {"overall_score": "number"},
            },
            "expectation_results": {
                "A": {"pass_rate": "number"},
                "B": {"pass_rate": "number"},
            },
        },
    }


def calculate_benchmark_stats(values: list[float]) -> dict[str, float]:
    if not values:
        return {"mean": 0.0, "stddev": 0.0, "min": 0.0, "max": 0.0}
    if len(values) == 1:
        value = round(float(values[0]), 4)
        return {"mean": value, "stddev": 0.0, "min": value, "max": value}

    sample_mean = sum(values) / len(values)
    variance = sum((value - sample_mean) ** 2 for value in values) / (len(values) - 1)
    stddev = variance ** 0.5
    return {
        "mean": round(sample_mean, 4),
        "stddev": round(stddev, 4),
        "min": round(min(values), 4),
        "max": round(max(values), 4),
    }


def load_comparison_index(skill_dir: Path) -> dict[int, dict[str, Any]]:
    comparisons_path = skill_dir / "blind-comparisons.json"
    if not comparisons_path.exists():
        return {}
    items = load_comparisons(comparisons_path)
    return {
        int(item.get("eval_id")): item
        for item in items
        if item.get("eval_id") is not None
    }


def configuration_side_for_eval(skill_dir: Path, eval_id: int) -> dict[str, str]:
    blind_map_path = skill_dir / f"eval-{eval_id}" / "blind-map.json"
    if not blind_map_path.exists():
        return {}
    mapping = read_json(blind_map_path)
    return {config: side for side, config in mapping.items()}


def build_skill_creator_benchmark(iteration_dir: Path, workspace_root: Path, skill_name: str) -> dict[str, Any]:
    skill_dir = iteration_dir / skill_name
    if not skill_dir.exists():
        raise FileNotFoundError(f"Missing skill results directory for '{skill_name}': {skill_dir}")

    eval_definition = load_skill_eval_definition(workspace_root, skill_name)
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
        comparison_item = comparison_index.get(int(eval_id))
        side_by_config = configuration_side_for_eval(skill_dir, int(eval_id))

        for configuration in ("with_skill", "without_skill"):
            summary = summaries.get(configuration)
            if not summary:
                missing_runs.append(f"{skill_name} {configuration}: missing summary JSON")
                continue

            eval_row = next((row for row in summary.get("evals", []) if row.get("id") == eval_id), None)
            if not eval_row:
                missing_runs.append(f"{skill_name} eval-{eval_id} {configuration}: missing response summary row")
                continue

            response_path = skill_dir / eval_row["response_path"]
            if not response_path.exists():
                missing_runs.append(f"{skill_name} eval-{eval_id} {configuration}: missing response file")
                continue

            pass_rate = None
            if comparison_item and side_by_config.get(configuration):
                expectation_results = comparison_item.get("expectation_results", {})
                side = side_by_config[configuration]
                pass_rate = expectation_results.get(side, {}).get("pass_rate")

            if pass_rate is None:
                missing_runs.append(f"{skill_name} eval-{eval_id} {configuration}: missing blind expectation pass rate")
                continue

            passed = int(round(float(pass_rate) * expectation_count)) if expectation_count else 0
            passed = max(0, min(expectation_count, passed))
            failed = max(0, expectation_count - passed)
            time_seconds = summary.get("summary", {}).get("elapsed_seconds_per_eval")

            runs.append(
                {
                    "eval_id": int(eval_id),
                    "eval_name": f"eval-{eval_id}",
                    "configuration": configuration,
                    "run_number": 1,
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
            "runs_per_configuration": 1,
        },
        "runs": runs,
        "run_summary": summary_by_config,
        "notes": notes,
    }


def write_skill_creator_benchmark(iteration_dir: Path, workspace_root: Path, skill_name: str, output_path: Path) -> dict[str, Any]:
    benchmark = build_skill_creator_benchmark(iteration_dir, workspace_root, skill_name)
    write_json(output_path, benchmark)
    markdown_lines = [
        f"# Skill-Creator Benchmark Export — {skill_name}",
        "",
        f"Iteration: {iteration_dir.name}",
        f"Included eval ids: {', '.join(map(str, benchmark['metadata']['evals_run'])) if benchmark['metadata']['evals_run'] else 'none'}",
        "",
        "## Notes",
        "",
    ]
    markdown_lines.extend(f"- {note}" for note in benchmark.get("notes", []))
    write_text(output_path.with_suffix(".md"), "\n".join(markdown_lines) + "\n")
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

    eval_definition = load_skill_eval_definition(workspace_root, skill_name)

    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    exported_runs: list[dict[str, Any]] = []
    missing_runs: list[dict[str, Any]] = []
    for eval_item in eval_definition.get("evals", []):
        eval_id = eval_item.get("id")
        if eval_id is None:
            continue
        for configuration in ("with_skill", "without_skill"):
            response_path = skill_dir / f"eval-{eval_id}" / configuration / "response.md"
            if not response_path.exists():
                missing_runs.append(
                    {
                        "eval_id": eval_id,
                        "configuration": configuration,
                        "expected_path": response_path.relative_to(workspace_root).as_posix(),
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
                    "expected_output": eval_item.get("expected_output", ""),
                    "assertions": eval_item.get("expectations", []),
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
    write_json(output_dir / "export-summary.json", summary)
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

    eval_definition = load_skill_eval_definition(workspace_root, skill_name)
    eval_entry = get_eval_entry(eval_definition, eval_id)
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
        "prompt": eval_entry.get("prompt"),
        "expected_output": eval_entry.get("expected_output"),
        "expectations": eval_entry.get("expectations", []),
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
            "evals_path": (workspace_root / ".github" / "skills" / skill_name / "evals" / "evals.json").relative_to(workspace_root).as_posix(),
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
        "MCP tools remain disabled for every benchmark agent.",
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

    return {
        "iteration": iteration_dir.name,
        "required_setting": {
            "chat.useCustomAgentHooks": True,
        },
        "agents": BENCHMARK_AGENTS,
        "baseline_isolation": baseline_isolation,
        "entrypoints": {
            "interactive": INTERACTIVE_ENTRYPOINT,
            "automation": AUTOMATION_ENTRYPOINT,
        },
        "phases": [
            {
                "phase": "without_skill",
                "agent": baseline_agent,
                "precondition": (
                    "Workspace skills were physically moved out of .github/skills/ and fresh workers were started afterwards."
                    if baseline_isolation != "hook-only"
                    else "Workspace skills may remain in place, but the baseline run is an explicit hook-only isolation probe."
                ),
            },
            {
                "phase": "with_skill",
                "agent": BENCHMARK_AGENTS["with_skill"],
                "precondition": "Workspace skills were restored and each fresh worker stays inside one target skill directory.",
                "target_skill": skill,
            },
            {
                "phase": "blind_compare",
                "agent": BENCHMARK_AGENTS["blind_compare"],
                "precondition": "Only blind A/B artifacts and the target eval definitions are exposed to the comparator.",
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
            blind_dir = eval_dir / "blind"
            if not blind_dir.exists():
                continue
            checked_evals += 1

            for required_name in ("A.md", "B.md"):
                if not (blind_dir / required_name).exists():
                    issues.append(
                        {
                            "skill": skill_dir.name,
                            "path": blind_dir.relative_to(iteration_dir).as_posix(),
                            "issue": f"missing {required_name}",
                        }
                    )

            extra_files = sorted(
                child.name
                for child in blind_dir.iterdir()
                if child.is_file() and child.name not in {"A.md", "B.md"}
            )
            if extra_files:
                issues.append(
                    {
                        "skill": skill_dir.name,
                        "path": blind_dir.relative_to(iteration_dir).as_posix(),
                        "issue": f"unexpected files in blind directory: {', '.join(extra_files)}",
                    }
                )

            if (blind_dir / "blind-map.json").exists():
                issues.append(
                    {
                        "skill": skill_dir.name,
                        "path": blind_dir.relative_to(iteration_dir).as_posix(),
                        "issue": "blind-map.json must stay outside the blind/ directory",
                    }
                )

            if not (eval_dir / "blind-map.json").exists():
                issues.append(
                    {
                        "skill": skill_dir.name,
                        "path": eval_dir.relative_to(iteration_dir).as_posix(),
                        "issue": "missing blind-map.json beside the eval directory",
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


def run_self_test(iteration_dir: Path, workspace_root: Path, baseline_isolation: str) -> dict[str, Any]:
    policy_test = run_command([sys.executable, "test/scripts/test_benchmark_agent_policy.py"], workspace_root)
    blind_isolation = validate_blind_isolation(iteration_dir)
    viewer_script = locate_skill_creator_viewer_script(workspace_root)
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
        "blind_isolation": blind_isolation,
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


def prepare_blind(iteration_dir: Path) -> dict[str, Any]:
    prepared: list[dict[str, Any]] = []
    for skill_dir in skill_dirs(iteration_dir):
        for eval_dir in sorted(skill_dir.glob("eval-*"), key=lambda path: path.name):
            with_response = eval_dir / "with_skill" / "response.md"
            without_response = eval_dir / "without_skill" / "response.md"
            if not with_response.exists() or not without_response.exists():
                continue

            blind_dir = eval_dir / "blind"
            blind_dir.mkdir(parents=True, exist_ok=True)

            seed = hashlib.sha256(f"{iteration_dir.name}:{skill_dir.name}:{eval_dir.name}".encode("utf-8")).hexdigest()
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
            write_json(eval_dir / "blind-map.json", mapping)

            prepared.append(
                {
                    "skill": skill_dir.name,
                    "eval": eval_dir.name,
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
    }


def comparison_metrics(skill_dir: Path, comparison_items: list[dict[str, Any]]) -> dict[str, Any]:
    with_win_count = 0
    without_win_count = 0
    ties = 0
    with_expectation_rates: list[float] = []
    without_expectation_rates: list[float] = []
    with_rubric_scores: list[float] = []
    without_rubric_scores: list[float] = []

    for item in comparison_items:
        eval_id = item.get("eval_id")
        eval_dir = skill_dir / f"eval-{eval_id}"
        blind_map_path = eval_dir / "blind-map.json"
        if not blind_map_path.exists():
            continue
        mapping = read_json(blind_map_path)
        reverse_mapping = {config: side for side, config in mapping.items()}

        winner = item.get("winner")
        if winner == "TIE":
            ties += 1
        elif mapping.get(winner) == "with_skill":
            with_win_count += 1
        elif mapping.get(winner) == "without_skill":
            without_win_count += 1

        expectation_results = item.get("expectation_results", {})
        rubric = item.get("rubric", {})

        with_side = reverse_mapping.get("with_skill")
        without_side = reverse_mapping.get("without_skill")

        if with_side and with_side in expectation_results:
            with_expectation_rates.append(expectation_results[with_side].get("pass_rate", 0.0))
        if without_side and without_side in expectation_results:
            without_expectation_rates.append(expectation_results[without_side].get("pass_rate", 0.0))

        if with_side and with_side in rubric:
            with_rubric_scores.append(rubric[with_side].get("overall_score", 0.0))
        if without_side and without_side in rubric:
            without_rubric_scores.append(rubric[without_side].get("overall_score", 0.0))

    total_resolved = with_win_count + without_win_count + ties
    with_win_rate = (with_win_count / total_resolved) if total_resolved else None
    without_win_rate = (without_win_count / total_resolved) if total_resolved else None

    with_expectation_mean = safe_mean(with_expectation_rates)
    without_expectation_mean = safe_mean(without_expectation_rates)
    with_rubric_mean = safe_mean(with_rubric_scores)
    without_rubric_mean = safe_mean(without_rubric_scores)

    return {
        "blind": {
            "with_skill_wins": with_win_count,
            "without_skill_wins": without_win_count,
            "ties": ties,
            "with_skill_win_rate": round_or_none(with_win_rate),
            "without_skill_win_rate": round_or_none(without_win_rate),
        },
        "expectation_pass_rate": {
            "with_skill": with_expectation_mean,
            "without_skill": without_expectation_mean,
            "delta": delta_or_none(with_expectation_mean, without_expectation_mean),
        },
        "rubric_score": {
            "with_skill": with_rubric_mean,
            "without_skill": without_rubric_mean,
            "delta": delta_or_none(with_rubric_mean, without_rubric_mean),
        },
        "comparison_count": total_resolved,
    }


def build_skill_row(skill_dir: Path, workspace_root: Path) -> dict[str, Any] | None:
    with_summary_path = skill_dir / "with_skill-summary.json"
    without_summary_path = skill_dir / "without_skill-summary.json"
    comparisons_path = skill_dir / "blind-comparisons.json"
    skill_eval_path = workspace_root / ".github" / "skills" / skill_dir.name / "evals" / "evals.json"

    if not with_summary_path.exists() or not without_summary_path.exists() or not comparisons_path.exists() or not skill_eval_path.exists():
        return None

    with_metrics = load_summary_metrics(with_summary_path)
    without_metrics = load_summary_metrics(without_summary_path)
    comparison_items = load_comparisons(comparisons_path)
    capability = comparison_metrics(skill_dir, comparison_items)
    eval_def = read_json(skill_eval_path)
    eval_count = len(eval_def.get("evals", []))

    return {
        "skill": skill_dir.name,
        "eval_count": eval_count,
        "capability": capability,
        "consumption": {
            "with_skill": {
                "response_words_per_eval": with_metrics.get("response_words_per_eval"),
                "files_read_count": with_metrics.get("files_read_count"),
                "files_written_count": with_metrics.get("files_written_count"),
            },
            "without_skill": {
                "response_words_per_eval": without_metrics.get("response_words_per_eval"),
                "files_read_count": without_metrics.get("files_read_count"),
                "files_written_count": without_metrics.get("files_written_count"),
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
            },
            "without_skill": {
                "elapsed_seconds_total": without_metrics.get("elapsed_seconds_total"),
                "elapsed_seconds_per_eval": without_metrics.get("elapsed_seconds_per_eval"),
            },
            "delta": {
                "elapsed_seconds_total": delta_or_none(with_metrics.get("elapsed_seconds_total"), without_metrics.get("elapsed_seconds_total")),
                "elapsed_seconds_per_eval": delta_or_none(with_metrics.get("elapsed_seconds_per_eval"), without_metrics.get("elapsed_seconds_per_eval")),
            },
        },
    }


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

    eval_rows: list[dict[str, Any]] = []
    total_words = 0

    for eval_item in eval_definition.get("evals", []):
        eval_id = eval_item.get("id")
        response_path = skill_dir / f"eval-{eval_id}" / config / "response.md"
        if not response_path.exists():
            raise FileNotFoundError(f"Missing response for {skill_dir.name} {config} eval-{eval_id}: {response_path}")

        response_text = response_path.read_text(encoding="utf-8")
        response_words = count_words(response_text)
        total_words += response_words
        eval_rows.append(
            {
                "id": eval_id,
                "response_path": response_path.relative_to(skill_dir).as_posix(),
                "response_words": response_words,
            }
        )

    eval_count = len(eval_rows)
    elapsed_seconds_total = metrics.get("elapsed_seconds_total")
    elapsed_seconds_per_eval = None
    if elapsed_seconds_total is not None and eval_count:
        elapsed_seconds_per_eval = round(float(elapsed_seconds_total) / eval_count, 4)

    summary = {
        "skill_name": metrics.get("skill_name", skill_dir.name),
        "configuration": metrics.get("configuration", config),
        "language": metrics.get("language", "English"),
        "mcp_used": bool(metrics.get("mcp_used", False)),
        "summary": {
            "elapsed_seconds_total": round_or_none(elapsed_seconds_total),
            "elapsed_seconds_per_eval": elapsed_seconds_per_eval,
            "response_words_total": total_words,
            "response_words_per_eval": round_or_none(total_words / eval_count) if eval_count else None,
            "files_read_count": metrics.get("files_read_count"),
            "files_written_count": metrics.get("files_written_count"),
        },
        "evals": eval_rows,
    }

    write_json(skill_dir / f"{config}-summary.json", summary)
    return summary


def aggregate_suite(iteration_dir: Path, workspace_root: Path) -> dict[str, Any]:
    test_root = iteration_dir.parent
    previous_iteration = find_previous_iteration(test_root, iteration_dir)
    previous_summary_path = previous_iteration / "suite-summary.json" if previous_iteration else None
    previous_summary = read_json(previous_summary_path) if previous_summary_path and previous_summary_path.exists() else None
    metric_validation = validate_iteration_metrics(iteration_dir)

    skill_rows = [row for row in (build_skill_row(skill_dir, workspace_root) for skill_dir in skill_dirs(iteration_dir)) if row]
    overview_rows = suite_overview_rows(skill_rows)

    suite_summary = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "iteration": iteration_dir.name,
        "previous_iteration": previous_iteration.name if previous_iteration else None,
        "skill_count": len(skill_rows),
        "suite_averages": {
            "with_skill_win_rate": safe_mean([row["capability"]["blind"]["with_skill_win_rate"] for row in skill_rows]),
            "expectation_delta": safe_mean([row["capability"]["expectation_pass_rate"]["delta"] for row in skill_rows]),
            "rubric_delta": safe_mean([row["capability"]["rubric_score"]["delta"] for row in skill_rows]),
            "time_delta_per_eval": safe_mean([row["time"]["delta"]["elapsed_seconds_per_eval"] for row in skill_rows]),
            "words_delta_per_eval": safe_mean([row["consumption"]["delta"]["response_words_per_eval"] for row in skill_rows]),
            "files_read_delta": safe_mean([row["consumption"]["delta"]["files_read_count"] for row in skill_rows]),
        },
        "metric_validation": metric_validation,
        "overview": overview_rows,
        "skills": skill_rows,
        "previous_iteration_comparison": None,
    }

    if previous_summary:
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
    if value is None:
        return "-"
    if percentage:
        return f"{value * 100:.1f}%"
    if isinstance(value, int):
        return str(value)
    return f"{value:.{digits}f}"


def markdown_table(headers: list[str], rows: list[list[str]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(row) + " |")
    return "\n".join(lines)


def render_markdown(summary: dict[str, Any]) -> str:
    metric_validation = summary.get("metric_validation") or {}
    lines = [
        f"# Skill Suite Summary — {summary['iteration']}",
        "",
        f"Generated at: {summary['generated_at']}",
        f"Previous iteration: {summary['previous_iteration'] or 'None found'}",
        f"Skill count: {summary['skill_count']}",
        "",
        "## Metric validation",
        "",
        f"Status: {metric_validation.get('status', 'unknown')}",
        f"Files checked: {metric_validation.get('checked_files', 0)}/{metric_validation.get('expected_files', 0)}",
        f"Issues: {metric_validation.get('issue_count', 0)}",
        "",
        "## Metric legend",
        "",
        "| Metric | Meaning | How to read it |",
        "| --- | --- | --- |",
        "| With-skill win rate | Share of blind comparisons won by the `with_skill` response. | Higher is better for the skill. Ties are not wins. |",
        "| Expectation pass rate | Average share of listed expectations satisfied by a response. | Higher is better. `Expectation Δ = with_skill - without_skill`. |",
        "| Rubric score | Blind comparator overall quality score on a 0-10 scale. | Higher is better. `Rubric Δ = with_skill - without_skill`. |",
        "| Time per eval | Average wall-clock seconds spent per eval. | Lower is faster. `Time Δ = with_skill - without_skill`, so a negative delta means the skill was faster. |",
        "| Words per eval | Average response length in words. | Lower means more concise, but not automatically better unless quality stays strong. |",
        "| Files read count | Count of repository files intentionally read during a run. | Proxy for context consumption. Higher means more repository context was consumed. |",
        "",
        "### Reading deltas",
        "",
        "- `Expectation Δ > 0`: the skill satisfied more listed expectations.",
        "- `Rubric Δ > 0`: the skill was judged better overall.",
        "- `Time Δ < 0`: the skill was faster.",
        "- `Words Δ < 0`: the skill was more concise.",
        "- `Files read Δ > 0`: the skill consumed more repository context.",
        "",
        "## Suite overview",
        "",
    ]

    if metric_validation.get("issues"):
        issue_headers = ["Skill", "Config", "Path", "Problem", "Missing keys"]
        issue_rows = []
        for issue in metric_validation["issues"]:
            issue_rows.append(
                [
                    issue.get("skill", "-"),
                    issue.get("configuration", "-"),
                    issue.get("path", "-"),
                    issue.get("problem", "-"),
                    ", ".join(issue.get("missing_keys", [])) if issue.get("missing_keys") else "-",
                ]
            )
        lines.extend([
            markdown_table(issue_headers, issue_rows),
            "",
        ])
    else:
        lines.extend([
            "All required run-metrics files were present and complete.",
            "",
        ])

    overview_headers = [
        "Skill",
        "Evals",
        "With-skill win rate",
        "Expectation Δ",
        "Rubric Δ",
        "Time Δ / eval (s)",
        "Words Δ / eval",
        "Files read Δ",
    ]
    overview_rows = []
    for row in summary["overview"]:
        overview_rows.append(
            [
                row["skill"],
                str(row["eval_count"]),
                format_number(row["with_skill_win_rate"], percentage=True),
                format_number(row["expectation_delta"], digits=3),
                format_number(row["rubric_delta"], digits=3),
                format_number(row["time_delta_per_eval"], digits=3),
                format_number(row["words_delta_per_eval"], digits=1),
                format_number(row["files_read_delta"], digits=1),
            ]
        )
    lines.append(markdown_table(overview_headers, overview_rows))

    lines.extend([
        "",
        "## Per-skill detailed comparison",
        "",
    ])

    detail_headers = [
        "Skill",
        "Exp pass with",
        "Exp pass without",
        "Rubric with",
        "Rubric without",
        "Sec/eval with",
        "Sec/eval without",
        "Words/eval with",
        "Words/eval without",
        "Files read with",
        "Files read without",
    ]
    detail_rows = []
    for skill in summary["skills"]:
        detail_rows.append(
            [
                skill["skill"],
                format_number(skill["capability"]["expectation_pass_rate"]["with_skill"], digits=3),
                format_number(skill["capability"]["expectation_pass_rate"]["without_skill"], digits=3),
                format_number(skill["capability"]["rubric_score"]["with_skill"], digits=3),
                format_number(skill["capability"]["rubric_score"]["without_skill"], digits=3),
                format_number(skill["time"]["with_skill"]["elapsed_seconds_per_eval"], digits=3),
                format_number(skill["time"]["without_skill"]["elapsed_seconds_per_eval"], digits=3),
                format_number(skill["consumption"]["with_skill"]["response_words_per_eval"], digits=1),
                format_number(skill["consumption"]["without_skill"]["response_words_per_eval"], digits=1),
                format_number(skill["consumption"]["with_skill"]["files_read_count"], digits=1),
                format_number(skill["consumption"]["without_skill"]["files_read_count"], digits=1),
            ]
        )
    lines.append(markdown_table(detail_headers, detail_rows))

    lines.extend([
        "",
        "## Previous-iteration comparison",
        "",
    ])

    previous = summary.get("previous_iteration_comparison")
    if previous and previous.get("skills"):
        previous_headers = [
            "Skill",
            "Prev win rate",
            "Curr win rate",
            "Δ win rate",
            "Prev expectation Δ",
            "Curr expectation Δ",
            "Δ expectation Δ",
            "Prev time Δ / eval",
            "Curr time Δ / eval",
            "Δ time Δ / eval",
        ]
        previous_rows = []
        for row in previous["skills"]:
            previous_rows.append(
                [
                    row["skill"],
                    format_number(row["previous_with_skill_win_rate"], percentage=True),
                    format_number(row["current_with_skill_win_rate"], percentage=True),
                    format_number(row["delta_with_skill_win_rate"], digits=3),
                    format_number(row["previous_expectation_delta"], digits=3),
                    format_number(row["current_expectation_delta"], digits=3),
                    format_number(row["delta_expectation_delta"], digits=3),
                    format_number(row["previous_time_delta_per_eval"], digits=3),
                    format_number(row["current_time_delta_per_eval"], digits=3),
                    format_number(row["delta_time_delta_per_eval"], digits=3),
                ]
            )
        lines.append(markdown_table(previous_headers, previous_rows))
    else:
        lines.append("No previous iteration was found for comparison.")

    return "\n".join(lines) + "\n"


def cmd_prepare_blind(args: argparse.Namespace) -> None:
    summary = prepare_blind(args.iteration)
    print(json.dumps(summary, indent=2, ensure_ascii=False))


def cmd_disable_workspace_skills(args: argparse.Namespace) -> None:
    summary = disable_workspace_skills(args.workspace_root, args.iteration)
    print(json.dumps(summary, indent=2, ensure_ascii=False))


def cmd_restore_workspace_skills(args: argparse.Namespace) -> None:
    summary = restore_workspace_skills(args.workspace_root, args.iteration)
    print(json.dumps(summary, indent=2, ensure_ascii=False))


def cmd_summarize_config(args: argparse.Namespace) -> None:
    summary = summarize_config(args.skill_dir, args.config, args.evals, args.metrics)
    print(json.dumps({
        "skill_name": summary["skill_name"],
        "configuration": summary["configuration"],
        "eval_count": len(summary["evals"]),
        "output_json": str(args.skill_dir / f"{args.config}-summary.json"),
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


def cmd_blind_compare_bundle(args: argparse.Namespace) -> None:
    bundle = build_blind_compare_bundle(args.iteration, args.workspace_root, args.skill, args.eval_id)
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
        "output_md": str(output_path.with_suffix('.md')),
        "run_count": len(benchmark.get("runs", [])),
        "note_count": len(benchmark.get("notes", [])),
    }, indent=2, ensure_ascii=False))


def cmd_validate_metrics(args: argparse.Namespace) -> None:
    summary = validate_iteration_metrics(args.iteration)
    print(json.dumps(summary, indent=2, ensure_ascii=False))


def cmd_normalize_metrics(args: argparse.Namespace) -> None:
    summary = normalize_iteration_metrics(args.iteration)
    print(json.dumps(summary, indent=2, ensure_ascii=False))


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
        started_at=args.started_at,
        finished_at=args.finished_at,
    )
    print(json.dumps(summary, indent=2, ensure_ascii=False))


def cmd_materialize_comparisons(args: argparse.Namespace) -> None:
    summary = materialize_blind_comparisons(args.iteration, args.skill, args.raw_json)
    print(json.dumps(summary, indent=2, ensure_ascii=False))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Utility helpers for the skill evaluation suite")
    subparsers = parser.add_subparsers(dest="command", required=True)

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
    summarize_parser.add_argument("--skill-dir", type=Path, required=True, help="Path to /test/iteration-N/<skill-name>")
    summarize_parser.add_argument("--config", choices=["with_skill", "without_skill"], required=True, help="Configuration name")
    summarize_parser.add_argument("--evals", type=Path, required=True, help="Path to the skill evals.json file")
    summarize_parser.add_argument("--metrics", type=Path, help="Optional path to the run-metrics JSON file")
    summarize_parser.set_defaults(func=cmd_summarize_config)

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
    write_metrics_parser.set_defaults(func=cmd_write_run_metrics)

    materialize_run_parser = subparsers.add_parser(
        "materialize-run",
        help="Write response.md files and canonical run-metrics.json from one raw benchmark worker JSON payload",
    )
    materialize_run_parser.add_argument("--iteration", type=Path, required=True, help="Path to /test/iteration-N")
    materialize_run_parser.add_argument("--skill", required=True, help="Target skill name")
    materialize_run_parser.add_argument("--configuration", choices=["with_skill", "without_skill"], required=True, help="Configuration name")
    materialize_run_parser.add_argument("--raw-json", type=Path, required=True, help="Path to the raw worker JSON payload")
    materialize_run_parser.add_argument("--started-at", help="Optional ISO-8601 UTC timestamp to override the raw payload start time")
    materialize_run_parser.add_argument("--finished-at", help="Optional ISO-8601 UTC timestamp to override the raw payload finish time")
    materialize_run_parser.set_defaults(func=cmd_materialize_run)

    materialize_comparisons_parser = subparsers.add_parser(
        "materialize-comparisons",
        help="Write blind-comparisons.json from one raw comparator JSON payload",
    )
    materialize_comparisons_parser.add_argument("--iteration", type=Path, required=True, help="Path to /test/iteration-N")
    materialize_comparisons_parser.add_argument("--skill", required=True, help="Target skill name")
    materialize_comparisons_parser.add_argument("--raw-json", type=Path, required=True, help="Path to the raw comparator JSON payload")
    materialize_comparisons_parser.set_defaults(func=cmd_materialize_comparisons)

    validate_parser = subparsers.add_parser("validate-metrics", help="Validate that every run-metrics file exists and contains all required non-null keys")
    validate_parser.add_argument("--iteration", type=Path, required=True, help="Path to /test/iteration-N")
    validate_parser.set_defaults(func=cmd_validate_metrics)

    normalize_parser = subparsers.add_parser("normalize-metrics", help="Normalize known legacy run-metrics aliases into the canonical benchmark schema")
    normalize_parser.add_argument("--iteration", type=Path, required=True, help="Path to /test/iteration-N")
    normalize_parser.set_defaults(func=cmd_normalize_metrics)

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

    blind_bundle_parser = subparsers.add_parser("blind-compare-bundle", help="Build the blind-comparison input bundle for one skill eval using the benchmark comparator playbook")
    blind_bundle_parser.add_argument("--iteration", type=Path, required=True, help="Path to /test/iteration-N")
    blind_bundle_parser.add_argument("--workspace-root", type=Path, required=True, help="Workspace root path")
    blind_bundle_parser.add_argument("--skill", required=True, help="Target skill name")
    blind_bundle_parser.add_argument("--eval-id", type=int, required=True, help="Eval id inside the skill evals.json")
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
    grader_bundle_parser.add_argument("--eval-id", type=int, required=True, help="Eval id inside the skill evals.json")
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

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
