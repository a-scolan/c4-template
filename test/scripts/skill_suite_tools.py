from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean
from typing import Any


ITERATION_RE = re.compile(r"^iteration-(\d+)$")
WORD_RE = re.compile(r"\S+")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


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

    return {
        "blind": {
            "with_skill_wins": with_win_count,
            "without_skill_wins": without_win_count,
            "ties": ties,
            "with_skill_win_rate": round_or_none(with_win_rate),
            "without_skill_win_rate": round_or_none(without_win_rate),
        },
        "expectation_pass_rate": {
            "with_skill": safe_mean(with_expectation_rates),
            "without_skill": safe_mean(without_expectation_rates),
            "delta": round_or_none((safe_mean(with_expectation_rates) or 0.0) - (safe_mean(without_expectation_rates) or 0.0)),
        },
        "rubric_score": {
            "with_skill": safe_mean(with_rubric_scores),
            "without_skill": safe_mean(without_rubric_scores),
            "delta": round_or_none((safe_mean(with_rubric_scores) or 0.0) - (safe_mean(without_rubric_scores) or 0.0)),
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
                "response_words_per_eval": round_or_none((with_metrics.get("response_words_per_eval") or 0.0) - (without_metrics.get("response_words_per_eval") or 0.0)),
                "files_read_count": round_or_none((with_metrics.get("files_read_count") or 0.0) - (without_metrics.get("files_read_count") or 0.0)),
                "files_written_count": round_or_none((with_metrics.get("files_written_count") or 0.0) - (without_metrics.get("files_written_count") or 0.0)),
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
                "elapsed_seconds_total": round_or_none((with_metrics.get("elapsed_seconds_total") or 0.0) - (without_metrics.get("elapsed_seconds_total") or 0.0)),
                "elapsed_seconds_per_eval": round_or_none((with_metrics.get("elapsed_seconds_per_eval") or 0.0) - (without_metrics.get("elapsed_seconds_per_eval") or 0.0)),
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
    metrics = read_json(metrics_file) if metrics_file.exists() else {}

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
            "files_written_count": metrics.get("files_written_count", eval_count),
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
                    "delta_with_skill_win_rate": round_or_none((row.get("with_skill_win_rate") or 0.0) - (previous_row.get("with_skill_win_rate") or 0.0)),
                    "previous_expectation_delta": previous_row.get("expectation_delta"),
                    "current_expectation_delta": row.get("expectation_delta"),
                    "delta_expectation_delta": round_or_none((row.get("expectation_delta") or 0.0) - (previous_row.get("expectation_delta") or 0.0)),
                    "previous_rubric_delta": previous_row.get("rubric_delta"),
                    "current_rubric_delta": row.get("rubric_delta"),
                    "delta_rubric_delta": round_or_none((row.get("rubric_delta") or 0.0) - (previous_row.get("rubric_delta") or 0.0)),
                    "previous_time_delta_per_eval": previous_row.get("time_delta_per_eval"),
                    "current_time_delta_per_eval": row.get("time_delta_per_eval"),
                    "delta_time_delta_per_eval": round_or_none((row.get("time_delta_per_eval") or 0.0) - (previous_row.get("time_delta_per_eval") or 0.0)),
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
    lines = [
        f"# Skill Suite Summary — {summary['iteration']}",
        "",
        f"Generated at: {summary['generated_at']}",
        f"Previous iteration: {summary['previous_iteration'] or 'None found'}",
        f"Skill count: {summary['skill_count']}",
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
        "output_json": str(args.iteration / "suite-summary.json"),
        "output_md": str(args.iteration / "suite-summary.md"),
    }, indent=2, ensure_ascii=False))


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

    aggregate_parser = subparsers.add_parser("aggregate", help="Aggregate per-skill results into suite-summary files")
    aggregate_parser.add_argument("--iteration", type=Path, required=True, help="Path to /test/iteration-N")
    aggregate_parser.add_argument("--workspace-root", type=Path, required=True, help="Workspace root path")
    aggregate_parser.set_defaults(func=cmd_aggregate)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
