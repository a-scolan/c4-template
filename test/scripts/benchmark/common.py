from __future__ import annotations

import os
import hashlib
import json
import re
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean
from typing import Any


WORD_RE = re.compile(r"\S+")


def _json_error_excerpt(text: str, pos: int, radius: int = 80) -> str:
	start = max(0, pos - radius)
	end = min(len(text), pos + radius)
	excerpt = text[start:end].replace("\r", "\\r").replace("\n", "\\n")
	if start > 0:
		excerpt = "…" + excerpt
	if end < len(text):
		excerpt = excerpt + "…"
	return excerpt


def read_json(path: Path) -> Any:
	text = path.read_text(encoding="utf-8")
	try:
		return json.loads(text)
	except json.JSONDecodeError as exc:
		excerpt = _json_error_excerpt(text, exc.pos)
		raise ValueError(
			f"Invalid JSON in {path} at line {exc.lineno}, column {exc.colno}: {exc.msg}. Context: {excerpt}"
		) from exc


def write_json(path: Path, data: Any) -> None:
	path.parent.mkdir(parents=True, exist_ok=True)
	serialized = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
	temp_path: Path | None = None
	try:
		with tempfile.NamedTemporaryFile(
			mode="w",
			encoding="utf-8",
			dir=path.parent,
			delete=False,
			prefix=f".{path.name}.",
			suffix=".tmp",
		) as handle:
			handle.write(serialized)
			handle.flush()
			os.fsync(handle.fileno())
			temp_path = Path(handle.name)
		if temp_path is None:
			raise RuntimeError(f"Failed to create temp file for JSON write: {path}")
		temp_path.replace(path)
	except Exception:
		if temp_path is not None and temp_path.exists():
			temp_path.unlink()
		raise


def write_text(path: Path, content: str) -> None:
	path.parent.mkdir(parents=True, exist_ok=True)
	path.write_text(content, encoding="utf-8")


def utc_now_iso() -> str:
	return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def deep_copy_json_like(value: Any) -> Any:
	return json.loads(json.dumps(value, ensure_ascii=False))


def file_sha256(path: Path) -> str:
	digest = hashlib.sha256()
	with path.open("rb") as handle:
		for chunk in iter(lambda: handle.read(65536), b""):
			digest.update(chunk)
	return digest.hexdigest()


def normalize_string_list(value: Any) -> list[str]:
	if not isinstance(value, list):
		return []
	normalized: list[str] = []
	for item in value:
		if isinstance(item, str) and item.strip():
			normalized.append(item.strip())
	return normalized


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


def delta_or_none(left: float | int | None, right: float | int | None, digits: int = 4) -> float | None:
	if left is None or right is None:
		return None
	return round(float(left) - float(right), digits)


def relative_to_root(path: Path, root: Path) -> str:
	return path.relative_to(root).as_posix()


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
