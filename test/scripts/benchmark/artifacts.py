from __future__ import annotations

import re
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .common import write_json


ITERATION_RE = re.compile(r"^iteration-(\d+)$")
SERIES_ITERATION_RE = re.compile(r"^.+-test\d+$")
REVIEW_EXPORT_DIR_RE = re.compile(r"^_skill-creator-review-workspace(?:-.+)?$")
REVIEW_EXPORT_FILES = {
    "skill-creator-review.html",
    "skill-creator-benchmark.json",
    "skill-creator-benchmark.md",
}


def is_benchmark_iteration_dir(name: str) -> bool:
    return bool(ITERATION_RE.match(name) or SERIES_ITERATION_RE.match(name))


def remove_path(path: Path) -> None:
    if path.is_dir():
        shutil.rmtree(path)
    else:
        path.unlink()


def _is_git_tracked(path: Path, workspace_root: Path) -> bool:
    """Check if a directory contains any git-tracked files."""
    try:
        rel = path.relative_to(workspace_root).as_posix()
        result = subprocess.run(
            ["git", "ls-files", "--error-unmatch", rel],
            cwd=workspace_root,
            capture_output=True,
            timeout=10,
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        return True  # assume tracked on error to avoid data loss


def clean_benchmark_artifacts(workspace_root: Path) -> dict[str, Any]:
    test_root = workspace_root / "test"
    removed: list[str] = []
    missing: list[str] = []
    skipped: list[str] = []

    targets: list[Path] = []
    if test_root.exists():
        targets.extend(
            sorted(
                [
                    child
                    for child in test_root.iterdir()
                    if child.is_dir() and is_benchmark_iteration_dir(child.name)
                ],
                key=lambda path: path.name,
            )
        )
        targets.extend(
            [
                test_root / "_agent-hooks",
                test_root / "_live-mcp-probe",
                test_root / "scripts" / "__pycache__",
            ]
        )

    for path in targets:
        relative = path.relative_to(workspace_root).as_posix()
        if not path.exists():
            missing.append(relative)
            continue
        if _is_git_tracked(path, workspace_root):
            skipped.append(relative)
            continue
        remove_path(path)
        removed.append(relative)

    summary = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "removed_count": len(removed),
        "removed": removed,
        "skipped_count": len(skipped),
        "skipped": skipped,
        "skipped_reason": "git-tracked directories are preserved to avoid data loss",
        "missing_count": len(missing),
        "missing": missing,
    }
    meta_root = test_root / "_meta"
    meta_root.mkdir(parents=True, exist_ok=True)
    write_json(meta_root / "clean-benchmark-artifacts.json", summary)
    return summary


def prune_generated_artifacts(iteration_dir: Path, workspace_root: Path) -> dict[str, Any]:
    removed: list[str] = []

    for child in sorted(iteration_dir.iterdir(), key=lambda path: path.name):
        if not child.is_dir() or child.name.startswith("_") or child.name == "scripts":
            continue

        for candidate in sorted(child.iterdir(), key=lambda path: path.name):
            if candidate.is_dir() and REVIEW_EXPORT_DIR_RE.match(candidate.name):
                remove_path(candidate)
                removed.append(candidate.relative_to(workspace_root).as_posix())
            elif candidate.is_file() and candidate.name in REVIEW_EXPORT_FILES:
                remove_path(candidate)
                removed.append(candidate.relative_to(workspace_root).as_posix())

    summary = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "iteration": iteration_dir.name,
        "removed_count": len(removed),
        "removed": removed,
    }
    write_json(iteration_dir / "_meta" / "generated-artifacts-pruned.json", summary)
    return summary
