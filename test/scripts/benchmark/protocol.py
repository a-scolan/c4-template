from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .common import file_sha256, read_json, write_json
from .evals import skill_eval_paths, validate_workspace_eval_artifacts, workspace_benchmark_skill_names


def protocol_manifest_path(workspace_root: Path, manifest_relative_path: Path, manifest_path: Path | None = None) -> Path:
	return manifest_path or (workspace_root / manifest_relative_path)


def build_protocol_manifest(
	workspace_root: Path,
	*,
	version: str,
	tracked_files: tuple[str, ...],
	eval_artifact_schema_version: int,
	comparator_schema_version: int,
) -> dict[str, Any]:
	tracked: list[dict[str, Any]] = []
	for rel_path in tracked_files:
		absolute = workspace_root / rel_path
		if not absolute.exists():
			raise FileNotFoundError(f"Missing protocol-tracked file: {absolute}")
		tracked.append(
			{
				"path": rel_path,
				"sha256": file_sha256(absolute),
			}
		)
	return {
		"protocol_version": version,
		"generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
		"eval_artifact_schema_version": eval_artifact_schema_version,
		"comparator_schema_version": comparator_schema_version,
		"tracked_files": tracked,
	}


def validate_protocol_manifest(workspace_root: Path, manifest_path: Path) -> dict[str, Any]:
	if not manifest_path.exists():
		raise FileNotFoundError(f"Missing protocol manifest: {manifest_path}")

	manifest = read_json(manifest_path)
	issues: list[dict[str, Any]] = []
	for item in manifest.get("tracked_files", []):
		rel_path = item.get("path")
		expected_hash = item.get("sha256")
		if not isinstance(rel_path, str) or not isinstance(expected_hash, str):
			issues.append({"path": rel_path or "<unknown>", "problem": "invalid manifest entry"})
			continue
		absolute = workspace_root / rel_path
		if not absolute.exists():
			issues.append({"path": rel_path, "problem": "missing file"})
			continue
		actual_hash = file_sha256(absolute)
		if actual_hash != expected_hash:
			issues.append(
				{
					"path": rel_path,
					"problem": "hash mismatch",
					"expected_sha256": expected_hash,
					"actual_sha256": actual_hash,
				}
			)

	return {
		"manifest_path": manifest_path.relative_to(workspace_root).as_posix(),
		"protocol_version": manifest.get("protocol_version"),
		"tracked_file_count": len(manifest.get("tracked_files", [])),
		"issue_count": len(issues),
		"issues": issues,
		"passed": len(issues) == 0,
	}


def freeze_protocol_for_iteration(
	iteration_dir: Path,
	workspace_root: Path,
	manifest_path: Path,
	*,
	evals_public_filename: str,
	grading_spec_filename: str,
) -> dict[str, Any]:
	manifest_validation = validate_protocol_manifest(workspace_root, manifest_path)
	if not manifest_validation.get("passed"):
		raise ValueError(f"Protocol manifest mismatch: {manifest_validation['issue_count']} issue(s)")

	eval_validation = validate_workspace_eval_artifacts(workspace_root, evals_public_filename, grading_spec_filename)
	if not eval_validation.get("passed"):
		raise ValueError(f"Split eval artifact validation failed: {eval_validation['issue_count']} issue(s)")

	skill_hashes: list[dict[str, Any]] = []
	for skill_name in workspace_benchmark_skill_names(workspace_root, evals_public_filename, grading_spec_filename):
		paths = skill_eval_paths(workspace_root, skill_name, evals_public_filename, grading_spec_filename)
		skill_hashes.append(
			{
				"skill": skill_name,
				"evals_public_path": paths["public"].relative_to(workspace_root).as_posix(),
				"evals_public_sha256": file_sha256(paths["public"]),
				"grading_spec_path": paths["grading"].relative_to(workspace_root).as_posix(),
				"grading_spec_sha256": file_sha256(paths["grading"]),
			}
		)

	manifest = read_json(manifest_path)
	lock_payload = {
		"generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
		"iteration": iteration_dir.name,
		"protocol_version": manifest.get("protocol_version"),
		"manifest_path": manifest_path.relative_to(workspace_root).as_posix(),
		"manifest_sha256": file_sha256(manifest_path),
		"tracked_files": manifest.get("tracked_files", []),
		"skill_eval_artifacts": skill_hashes,
	}
	output_path = iteration_dir / "_meta" / "protocol-lock.json"
	write_json(output_path, lock_payload)
	return {
		"iteration": iteration_dir.name,
		"protocol_version": lock_payload["protocol_version"],
		"manifest_path": lock_payload["manifest_path"],
		"output_path": output_path.relative_to(workspace_root).as_posix(),
		"tracked_file_count": len(lock_payload["tracked_files"]),
		"skill_count": len(skill_hashes),
	}
