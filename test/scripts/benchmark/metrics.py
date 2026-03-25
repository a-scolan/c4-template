from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from .common import coerce_bool, coerce_float, coerce_int, iso_to_datetime, read_json, write_json


RUN_DIR_RE = re.compile(r"^run-(\d+)$")


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


def parse_eval_metrics_path(path: Path, eval_metrics_re: re.Pattern[str]) -> int | None:
	match = eval_metrics_re.match(path.stem)
	return int(match.group(1)) if match else None


def infer_run_metrics_fields(metrics_path: Path) -> dict[str, str | None]:
	configuration = None
	file_name = metrics_path.name
	for candidate in ("with_skill", "without_skill"):
		if file_name == f"{candidate}-run-metrics.json":
			configuration = candidate
			break
		if metrics_path.parent.name == candidate:
			configuration = candidate
			break
		if metrics_path.parent.parent.name == candidate:
			configuration = candidate
			break

	skill_name = None
	if metrics_path.parent.name in {"with_skill", "without_skill"} and metrics_path.parent.parent.name == "_runs":
		skill_name = metrics_path.parent.parent.parent.name
	elif metrics_path.parent.parent.name in {"with_skill", "without_skill"} and metrics_path.parent.parent.parent.name == "_runs":
		skill_name = metrics_path.parent.parent.parent.parent.name
	elif metrics_path.parent != metrics_path:
		skill_name = metrics_path.parent.name
	return {
		"skill_name": skill_name,
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
	run_number: int | None = None,
) -> dict[str, Any]:
	payload = {
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
	if run_number is not None:
		payload["run_number"] = run_number
	return payload


def canonicalize_run_metrics(
	metrics: dict[str, Any],
	metrics_path: Path | None = None,
	*,
	required_run_metric_keys: tuple[str, ...],
	run_metric_key_aliases: dict[str, tuple[str, ...]],
	run_metric_list_fallbacks: dict[str, tuple[str, ...]],
	run_metric_defaults: dict[str, Any],
	run_metric_alias_keys_to_drop: set[str],
) -> tuple[dict[str, Any], list[str]]:
	inferred = infer_run_metrics_fields(metrics_path) if metrics_path else {}
	canonical: dict[str, Any] = {}
	changes: list[str] = []

	for key in required_run_metric_keys:
		aliases = run_metric_key_aliases.get(key, (key,))
		value = None
		source_key = None
		for alias in aliases:
			if alias in metrics and metrics[alias] is not None:
				value = metrics[alias]
				source_key = alias
				break

		if value is None and key in run_metric_list_fallbacks:
			for list_key in run_metric_list_fallbacks[key]:
				list_value = metrics.get(list_key)
				if isinstance(list_value, list):
					value = len(list_value)
					source_key = list_key
					changes.append(f"derived {key} from {list_key}")
					break

		if value is None and inferred.get(key) is not None:
			value = inferred[key]
			changes.append(f"inferred {key} from metrics path")

		if value is None and key in run_metric_defaults:
			value = run_metric_defaults[key]
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

	normalized = {key: canonical.get(key) for key in required_run_metric_keys}
	for key, value in metrics.items():
		if key in normalized or key in run_metric_alias_keys_to_drop:
			continue
		normalized[key] = value

	return normalized, changes


def load_run_metrics(
	metrics_path: Path,
	*,
	write_back: bool,
	required_run_metric_keys: tuple[str, ...],
	run_metric_key_aliases: dict[str, tuple[str, ...]],
	run_metric_list_fallbacks: dict[str, tuple[str, ...]],
	run_metric_defaults: dict[str, Any],
	run_metric_alias_keys_to_drop: set[str],
) -> tuple[dict[str, Any], list[str]]:
	metrics = read_json(metrics_path)
	normalized, changes = canonicalize_run_metrics(
		metrics,
		metrics_path,
		required_run_metric_keys=required_run_metric_keys,
		run_metric_key_aliases=run_metric_key_aliases,
		run_metric_list_fallbacks=run_metric_list_fallbacks,
		run_metric_defaults=run_metric_defaults,
		run_metric_alias_keys_to_drop=run_metric_alias_keys_to_drop,
	)
	if write_back and (changes or normalized != metrics):
		write_json(metrics_path, normalized)
	return normalized, changes


def validate_run_metrics_payload(metrics: dict[str, Any], required_run_metric_keys: tuple[str, ...]) -> list[str]:
	return [key for key in required_run_metric_keys if key not in metrics or metrics[key] is None]
