from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .common import normalize_string_list, read_json


def validate_execution_check_definition(skill_name: str, owner_id: int | str, check_index: int, check: Any) -> list[str]:
	issues: list[str] = []
	if not isinstance(check, dict):
		return [f"{skill_name}: grading-spec {owner_id!r} execution_checks[{check_index}] must be an object"]
	if not isinstance(check.get("name"), str) or not check.get("name", "").strip():
		issues.append(f"{skill_name}: grading-spec {owner_id!r} execution_checks[{check_index}] must provide a non-empty name")
	for key in ("description", "when"):
		if key in check and (not isinstance(check.get(key), str) or not check.get(key, "").strip()):
			issues.append(f"{skill_name}: grading-spec {owner_id!r} execution_checks[{check_index}] field '{key}' must be a non-empty string when provided")
	if not isinstance(check.get("instructions"), list) or not check.get("instructions") or not all(isinstance(step, str) and step.strip() for step in check.get("instructions", [])):
		issues.append(f"{skill_name}: grading-spec {owner_id!r} execution_checks[{check_index}] must provide a non-empty string-only instructions list")
	for key in ("success_signals", "failure_signals"):
		if key in check and (not isinstance(check.get(key), list) or not all(isinstance(signal, str) and signal.strip() for signal in check.get(key, []))):
			issues.append(f"{skill_name}: grading-spec {owner_id!r} execution_checks[{check_index}] field '{key}' must be a string-only list when provided")
	return issues


def validate_execution_check_list(skill_name: str, owner_id: int | str, execution_checks: Any) -> list[str]:
	issues: list[str] = []
	if not isinstance(execution_checks, list) or not execution_checks:
		issues.append(f"{skill_name}: grading-spec {owner_id!r} execution_checks must be a non-empty array when provided")
		return issues
	for check_index, check in enumerate(execution_checks):
		issues.extend(validate_execution_check_definition(skill_name, owner_id, check_index, check))
	return issues


def workspace_skills_root(workspace_root: Path) -> Path:
	return workspace_root / ".github" / "skills"


def skill_eval_root(workspace_root: Path, skill_name: str) -> Path:
	return workspace_root / ".github" / "skills" / skill_name / "evals"


def skill_eval_paths(workspace_root: Path, skill_name: str, evals_public_filename: str, grading_spec_filename: str) -> dict[str, Path]:
	eval_root = skill_eval_root(workspace_root, skill_name)
	return {
		"root": eval_root,
		"public": eval_root / evals_public_filename,
		"grading": eval_root / grading_spec_filename,
	}


def workspace_benchmark_skill_names(workspace_root: Path, evals_public_filename: str, grading_spec_filename: str) -> list[str]:
	skills_root = workspace_skills_root(workspace_root)
	if not skills_root.exists():
		return []
	result: list[str] = []
	for child in sorted(skills_root.iterdir(), key=lambda path: path.name):
		if not child.is_dir():
			continue
		eval_root = child / "evals"
		if not eval_root.exists():
			continue
		if any((eval_root / name).exists() for name in (evals_public_filename, grading_spec_filename)):
			result.append(child.name)
	return result


def validate_public_eval_definition(skill_name: str, data: dict[str, Any]) -> list[str]:
	issues: list[str] = []
	if not isinstance(data, dict):
		return [f"{skill_name}: evals-public payload must be a JSON object"]

	if data.get("artifact_type") not in {None, "evals-public"}:
		issues.append(f"{skill_name}: evals-public artifact_type must be 'evals-public'")

	evals = data.get("evals")
	if not isinstance(evals, list) or not evals:
		issues.append(f"{skill_name}: evals-public must contain a non-empty 'evals' array")
		return issues

	seen_ids: set[int] = set()
	for index, item in enumerate(evals):
		if not isinstance(item, dict):
			issues.append(f"{skill_name}: evals-public eval #{index} must be an object")
			continue
		eval_id = item.get("id")
		if not isinstance(eval_id, int):
			issues.append(f"{skill_name}: evals-public eval #{index} must provide an integer id")
		elif eval_id in seen_ids:
			issues.append(f"{skill_name}: duplicate eval id {eval_id} in evals-public")
		else:
			seen_ids.add(eval_id)
		if not isinstance(item.get("prompt"), str) or not item.get("prompt", "").strip():
			issues.append(f"{skill_name}: eval {eval_id!r} in evals-public must provide a non-empty prompt")
		if "expected_output" in item or "expectations" in item:
			issues.append(f"{skill_name}: eval {eval_id!r} in evals-public leaks hidden grading fields")
		if "files" in item and not isinstance(item.get("files"), list):
			issues.append(f"{skill_name}: eval {eval_id!r} in evals-public must use a list for files")
	return issues


def validate_grading_spec_definition(skill_name: str, data: dict[str, Any]) -> list[str]:
	issues: list[str] = []
	if not isinstance(data, dict):
		return [f"{skill_name}: grading-spec payload must be a JSON object"]

	if data.get("artifact_type") not in {None, "grading-spec"}:
		issues.append(f"{skill_name}: grading-spec artifact_type must be 'grading-spec'")

	evals = data.get("evals")
	if not isinstance(evals, list) or not evals:
		issues.append(f"{skill_name}: grading-spec must contain a non-empty 'evals' array")
		return issues

	default_execution_checks = data.get("default_execution_checks")
	if default_execution_checks is not None:
		issues.extend(validate_execution_check_list(skill_name, "default", default_execution_checks))

	seen_ids: set[int] = set()
	for index, item in enumerate(evals):
		if not isinstance(item, dict):
			issues.append(f"{skill_name}: grading-spec eval #{index} must be an object")
			continue
		eval_id = item.get("id")
		if not isinstance(eval_id, int):
			issues.append(f"{skill_name}: grading-spec eval #{index} must provide an integer id")
		elif eval_id in seen_ids:
			issues.append(f"{skill_name}: duplicate eval id {eval_id} in grading-spec")
		else:
			seen_ids.add(eval_id)
		if "prompt" in item:
			issues.append(
				f"{skill_name}: grading-spec eval {eval_id!r} must not contain prompt; prompts live in evals-public"
			)
		if "files" in item and not isinstance(item.get("files"), list):
			issues.append(f"{skill_name}: grading-spec eval {eval_id!r} must use a list for files")
		if not isinstance(item.get("expected_output"), str):
			issues.append(f"{skill_name}: grading-spec eval {eval_id!r} must provide a string expected_output")
		expectations = item.get("expectations")
		if not isinstance(expectations, list) or not all(isinstance(entry, str) and entry.strip() for entry in expectations):
			issues.append(f"{skill_name}: grading-spec eval {eval_id!r} must provide a string-only expectations list")
		execution_checks = item.get("execution_checks")
		if execution_checks is not None:
			issues.extend(validate_execution_check_list(skill_name, f"eval {eval_id!r}", execution_checks))
	return issues


def validate_split_eval_pair(skill_name: str, public: dict[str, Any], grading: dict[str, Any]) -> list[str]:
	issues = validate_public_eval_definition(skill_name, public)
	issues.extend(validate_grading_spec_definition(skill_name, grading))
	if issues:
		return issues

	public_by_id = {item.get("id"): item for item in public.get("evals", []) if isinstance(item, dict)}
	grading_by_id = {item.get("id"): item for item in grading.get("evals", []) if isinstance(item, dict)}
	if set(public_by_id) != set(grading_by_id):
		issues.append(f"{skill_name}: eval ids differ between evals-public and grading-spec")
		return issues

	for eval_id in sorted(public_by_id):
		public_files = normalize_string_list(public_by_id[eval_id].get("files", []))
		grading_files = normalize_string_list(grading_by_id[eval_id].get("files", []))
		if public_files != grading_files:
			issues.append(f"{skill_name}: eval {eval_id} files differ between evals-public and grading-spec")
	return issues


def load_split_eval_artifacts(workspace_root: Path, skill_name: str, evals_public_filename: str, grading_spec_filename: str) -> dict[str, Any]:
	paths = skill_eval_paths(workspace_root, skill_name, evals_public_filename, grading_spec_filename)
	if paths["public"].exists():
		public = read_json(paths["public"])
	else:
		raise FileNotFoundError(f"Missing {evals_public_filename} for skill '{skill_name}': {paths['public']}")

	if paths["grading"].exists():
		grading = read_json(paths["grading"])
	else:
		raise FileNotFoundError(f"Missing {grading_spec_filename} for skill '{skill_name}': {paths['grading']}")

	issues = validate_split_eval_pair(skill_name, public, grading)
	if issues:
		raise ValueError("; ".join(issues))

	return {
		"skill_name": skill_name,
		"public": public,
		"grading": grading,
		"paths": paths,
	}


def validate_workspace_eval_artifacts(workspace_root: Path, evals_public_filename: str, grading_spec_filename: str) -> dict[str, Any]:
	issues: list[dict[str, Any]] = []
	skills_checked = 0
	for skill_name in workspace_benchmark_skill_names(workspace_root, evals_public_filename, grading_spec_filename):
		skills_checked += 1
		try:
			artifacts = load_split_eval_artifacts(workspace_root, skill_name, evals_public_filename, grading_spec_filename)
		except Exception as exc:
			issues.append({"skill": skill_name, "problem": str(exc)})
			continue

		public_path = artifacts["paths"]["public"]
		grading_path = artifacts["paths"]["grading"]
		if not public_path.exists():
			issues.append({"skill": skill_name, "problem": f"missing {evals_public_filename}"})
		if not grading_path.exists():
			issues.append({"skill": skill_name, "problem": f"missing {grading_spec_filename}"})

	return {
		"generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
		"skills_checked": skills_checked,
		"issue_count": len(issues),
		"issues": issues,
		"passed": len(issues) == 0,
	}
