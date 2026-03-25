"""
One-shot script: copy test/iteration-2 -> test/likec4-dsl-test2 and re-aggregate
with test/likec4-dsl-test as the previous iteration.

Run from workspace root:
    python test/scripts/setup_likec4_dsl_test2.py
"""
from __future__ import annotations

import json
import os
import shutil
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
WORKSPACE_ROOT = Path(".")
TEST_ROOT = WORKSPACE_ROOT / "test"
SOURCE_DIR = TEST_ROOT / "iteration-2"
TARGET_DIR = TEST_ROOT / "likec4-dsl-test2"
PREVIOUS_DIR = TEST_ROOT / "likec4-dsl-test"
SKIP_DIRS = {"_disabled-skills"}


def replace_iteration_label(text: str) -> str:
    return text.replace('"iteration-2"', '"likec4-dsl-test2"').replace(
        "iteration-2/", "likec4-dsl-test2/"
    ).replace(
        "test/iteration-2", "test/likec4-dsl-test2"
    )


def copy_tree(src: Path, dst: Path) -> int:
    """Copy src to dst (creating dst), skipping SKIP_DIRS. Returns count of copied files."""
    dst.mkdir(parents=True, exist_ok=True)
    count = 0
    for item in src.iterdir():
        if item.name in SKIP_DIRS:
            continue
        dest_item = dst / item.name
        if item.is_dir():
            count += copy_tree(item, dest_item)
        else:
            content = item.read_bytes()
            # For text/json files, patch iteration label references
            if item.suffix in {".json", ".md", ".txt"}:
                try:
                    text = content.decode("utf-8")
                    patched = replace_iteration_label(text)
                    dest_item.write_text(patched, encoding="utf-8")
                except UnicodeDecodeError:
                    dest_item.write_bytes(content)
            else:
                dest_item.write_bytes(content)
            count += 1
    return count


# ---------------------------------------------------------------------------
# Bootstrap: ensure skill_suite_tools is importable
# ---------------------------------------------------------------------------
SCRIPTS_DIR = str(Path("test/scripts").resolve())
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

import skill_suite_tools as sst  # noqa: E402

# ---------------------------------------------------------------------------
# Step 0: clean up any probe file left from tool test
# ---------------------------------------------------------------------------
probe = TEST_ROOT / "scripts" / "_probe.txt"
if probe.exists():
    probe.unlink()
    print("Removed probe file.")

# ---------------------------------------------------------------------------
# Step 1: Copy iteration-2 -> likec4-dsl-test2
# ---------------------------------------------------------------------------
if TARGET_DIR.exists():
    print(f"Target directory {TARGET_DIR} already exists — removing it first.")
    shutil.rmtree(TARGET_DIR)

print(f"Copying {SOURCE_DIR} -> {TARGET_DIR} (excluding {SKIP_DIRS}) ...")
copied = copy_tree(SOURCE_DIR, TARGET_DIR)
print(f"  Copied {copied} files.")

# Also update the protocol-lock iteration name
protocol_lock = TARGET_DIR / "_meta" / "protocol-lock.json"
if protocol_lock.exists():
    data = json.loads(protocol_lock.read_text(encoding="utf-8"))
    data["iteration"] = "likec4-dsl-test2"
    protocol_lock.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("  Updated protocol-lock.json iteration label.")

# ---------------------------------------------------------------------------
# Step 2: Monkey-patch find_previous_iteration so it returns likec4-dsl-test
# ---------------------------------------------------------------------------
_original_find = sst.find_previous_iteration


def _patched_find(test_root: Path, current_iteration: Path, override: Path | None = None) -> Path | None:  # type: ignore[override]
    if override is not None:
        return override if override.is_dir() else None
    if current_iteration.name == "likec4-dsl-test2":
        return PREVIOUS_DIR if PREVIOUS_DIR.is_dir() else None
    return _original_find(test_root, current_iteration)


sst.find_previous_iteration = _patched_find  # type: ignore[assignment]

# ---------------------------------------------------------------------------
# Step 3: Re-run aggregate for likec4-dsl-test2
# ---------------------------------------------------------------------------
print(f"\nRunning aggregate_suite for {TARGET_DIR.name} ...")
summary = sst.aggregate_suite(TARGET_DIR, WORKSPACE_ROOT)
out_json = TARGET_DIR / "suite-summary.json"
out_md = TARGET_DIR / "suite-summary.md"
sst.write_json(out_json, summary)
sst.write_text(out_md, sst.render_markdown(summary))
print(f"  previous_iteration: {summary.get('previous_iteration')}")
print(f"  skill_count: {summary.get('skill_count')}")
print(f"  with_skill_win_rate: {summary.get('suite_averages', {}).get('with_skill_win_rate')}")
print(f"  Written: {out_json}")
print(f"  Written: {out_md}")

# ---------------------------------------------------------------------------
# Step 4: Re-run write-static-review for likec4-dsl-test2 / likec4-dsl
# ---------------------------------------------------------------------------
print("\nRunning write_static_review ...")
output_html = TARGET_DIR / "likec4-dsl" / "skill-creator-review.html"
try:
    result = sst.write_static_review(TARGET_DIR, WORKSPACE_ROOT, "likec4-dsl", output_html)
    print(f"  Written HTML: {result.get('output_html')}")
    previous_ws = result.get("previous_workspace")
    if previous_ws:
        print(f"  Previous workspace: {previous_ws}")
    else:
        print("  WARNING: previous workspace was not included in HTML review.")
except Exception as exc:
    print(f"  ERROR generating static review: {exc}")
    import traceback
    traceback.print_exc()

print("\nDone.")
