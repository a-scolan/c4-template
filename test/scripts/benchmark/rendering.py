from __future__ import annotations

from typing import Any


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
	suite_variance = summary.get("suite_variance") or {}
	comparison_validity = summary.get("comparison_validity") or {}
	lines = [
		f"# Skill Suite Summary — {summary['iteration']}",
		"",
		f"Generated at: {summary['generated_at']}",
		f"Previous iteration: {summary['previous_iteration'] or 'None found'}",
		f"Protocol version: {summary.get('protocol_version') or 'unlocked'}",
		f"Skill count: {summary['skill_count']}",
		"",
	]

	if comparison_validity.get("provisional"):
		lines.extend([
			"## Benchmark caveats",
			"",
			"This iteration should be treated as **provisional**.",
			"",
		])
		for reason in comparison_validity.get("reasons", []):
			lines.append(f"- {reason}")
		for note in comparison_validity.get("protocol_deviations", []):
			lines.append(f"- Protocol deviation: {note}")
		for note in comparison_validity.get("notes", []):
			lines.append(f"- Note: {note}")
		lines.extend([
			"",
		])

	lines.extend([
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
		"| Executable validity | Share of snippet-bearing eval runs whose LikeC4 snippets passed automated structural checks. | Higher is better. `Executable Δ = with_skill - without_skill`. |",
		"",
		"### Reading deltas",
		"",
		"- `Expectation Δ > 0`: the skill satisfied more listed expectations.",
		"- `Rubric Δ > 0`: the skill was judged better overall.",
		"- `Time Δ < 0`: the skill was faster.",
		"- `Words Δ < 0`: the skill was more concise.",
		"- `Files read Δ > 0`: the skill consumed more repository context.",
		"- `Executable Δ > 0`: the skill produced more structurally valid LikeC4 snippets.",
		"",
		"## Suite variance",
		"",
	])

	variance_rows = []
	for metric_name, stats in (
		("With-skill win rate", suite_variance.get("with_skill_win_rate")),
		("Expectation Δ", suite_variance.get("expectation_delta")),
		("Rubric Δ", suite_variance.get("rubric_delta")),
		("Time Δ / eval", suite_variance.get("time_delta_per_eval")),
		("Executable Δ", suite_variance.get("executable_delta")),
	):
		if not stats:
			continue
		variance_rows.append(
			[
				metric_name,
				format_number(stats.get("mean"), digits=3),
				format_number(stats.get("stddev"), digits=3),
				format_number(stats.get("min"), digits=3),
				format_number(stats.get("max"), digits=3),
			]
		)
	if variance_rows:
		lines.extend([
			markdown_table(["Metric", "Mean", "Stddev", "Min", "Max"], variance_rows),
			"",
		])
	else:
		lines.extend([
			"Variance metrics are not available yet.",
			"",
		])

	lines.extend([
		"",
		"## Suite overview",
		"",
	])

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
		"Runs",
		"With-skill win rate",
		"Expectation Δ",
		"Rubric Δ",
		"Time Δ / eval (s)",
		"Executable Δ",
		"Words Δ / eval",
		"Files read Δ",
		"High-var evals",
	]
	overview_rows = []
	for row in summary["overview"]:
		overview_rows.append(
			[
				row["skill"],
				str(row["eval_count"]),
				str(row.get("run_count", 1)),
				format_number(row["with_skill_win_rate"], percentage=True),
				format_number(row["expectation_delta"], digits=3),
				format_number(row["rubric_delta"], digits=3),
				format_number(row["time_delta_per_eval"], digits=3),
				format_number(row.get("executable_delta"), digits=3),
				format_number(row["words_delta_per_eval"], digits=1),
				format_number(row["files_read_delta"], digits=1),
				str(row.get("high_variance_eval_count", 0)),
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
		"Runs",
		"Exp pass with",
		"Exp pass without",
		"Rubric with",
		"Rubric without",
		"Sec/eval with",
		"Sec/eval without",
		"Exec with",
		"Exec without",
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
				str(skill.get("run_count", 1)),
				format_number(skill["capability"]["expectation_pass_rate"]["with_skill"], digits=3),
				format_number(skill["capability"]["expectation_pass_rate"]["without_skill"], digits=3),
				format_number(skill["capability"]["rubric_score"]["with_skill"], digits=3),
				format_number(skill["capability"]["rubric_score"]["without_skill"], digits=3),
				format_number(skill["time"]["with_skill"]["elapsed_seconds_per_eval"], digits=3),
				format_number(skill["time"]["without_skill"]["elapsed_seconds_per_eval"], digits=3),
				format_number(skill["executable_validity"]["with_skill"].get("valid_eval_rate") if skill["executable_validity"]["with_skill"] else None, digits=3),
				format_number(skill["executable_validity"]["without_skill"].get("valid_eval_rate") if skill["executable_validity"]["without_skill"] else None, digits=3),
				format_number(skill["consumption"]["with_skill"]["response_words_per_eval"], digits=1),
				format_number(skill["consumption"]["without_skill"]["response_words_per_eval"], digits=1),
				format_number(skill["consumption"]["with_skill"]["files_read_count"], digits=1),
				format_number(skill["consumption"]["without_skill"]["files_read_count"], digits=1),
			]
		)
	lines.append(markdown_table(detail_headers, detail_rows))

	lines.extend([
		"",
		"## High-variance evals",
		"",
	])

	high_variance_evals = summary.get("high_variance_evals") or []
	if high_variance_evals:
		variance_headers = ["Skill", "Source", "Eval", "Run count", "Winner flips", "Expectation stddev", "Rubric stddev"]
		variance_rows = []
		for item in high_variance_evals:
			variance_rows.append(
				[
					item.get("skill", "-"),
					item.get("source", "-"),
					str(item.get("id", "-")),
					str(item.get("run_count", "-")),
					"yes" if item.get("winner_flips") else "no",
					format_number((item.get("expectation_delta_stats") or {}).get("stddev"), digits=3),
					format_number((item.get("rubric_delta_stats") or {}).get("stddev"), digits=3),
				]
			)
		lines.append(markdown_table(variance_headers, variance_rows))
	else:
		lines.append("No high-variance evals were flagged.")

	lines.extend([
		"",
		"## Previous-iteration comparison",
		"",
	])

	previous = summary.get("previous_iteration_comparison")
	if previous and previous.get("status") == "suppressed":
		lines.append("Cross-iteration comparison was suppressed for this iteration:")
		lines.append("")
		for reason in previous.get("reasons", []):
			lines.append(f"- {reason}")
	elif previous and previous.get("skills"):
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
