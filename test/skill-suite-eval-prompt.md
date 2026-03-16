# Skill Suite Evaluation Prompt

## Goal

Evaluate every workspace skill under `.github/skills/*` that provides split benchmark eval artifacts.

Run every eval prompt twice:

1. **with_skill**: explicitly read and follow the target skill.
2. **without_skill**: do not read any skill file; solve from general reasoning and repository context only.

All generated artifacts must live **only** under `/test`.
All written reports and result files must be **in English**.
All logs and reports must stay **anonymous**: never expose the absolute workspace path and never dump the repository tree.

## Hard constraints

- Do **not** use any MCP tool outside the scored `with_skill` / `without_skill` worker phases.
- In scored `with_skill` and `without_skill` workers only, all LikeC4 MCP tools (`likec4/*`) are allowed.
- The benchmark manager, blind comparator, and grader/analyzer-style review tasks must keep MCP disabled.
- Keep the runs isolated per skill.
- Do not edit repository source files while evaluating.
- Treat each skill as an independent benchmark target.
- Produce a **blind comparison** between `with_skill` and `without_skill` for every eval.
- If a previous iteration exists under `/test/iteration-*`, include a comparison against the latest previous iteration.
- No Git history mining is required.
- Do **not** log request or response character counts.
- Use a **fresh session or fresh worker** for each `<skill, configuration>` pair.
- In `with_skill`, enable only the single target skill.
- In `without_skill`, read **no** `SKILL.md` file at all.
- In `without_skill`, “without skill” means “do not read any `SKILL.md` file”; it does **not** mean “without allowed LikeC4 MCP tools”.
- A run is invalid if its `*-run-metrics.json` file is missing required keys or contains `null` for required metric values.
- Do **not** hand-author `*-run-metrics.json` files; write them with `python test/scripts/skill_suite_tools.py write-run-metrics ...`.
- **Critically important:** prompt-level instructions are **not enough** to guarantee a clean `without_skill` baseline.
- Before any `without_skill` run, physically disable workspace skills by moving every directory from `.github/skills/` into `test/iteration-N/_disabled-skills/`.
- Run **all** `without_skill` scenarios first while skills are physically disabled.
- Restore the skill directories back into `.github/skills/` only after the baseline batch is fully complete.
- Run `with_skill` scenarios **only after** restoration, in fresh workers created after the restore step.
- Default scheduler: execute independent workers in parallel within a phase; use serial fallback only when output paths would collide or runtime limits force it.
- If you intentionally run a hook-only baseline probe, label it as experimental and keep it separate from the strict relocated baseline results.

## Workspace scope

- Benchmark targets: `.github/skills/<skill-name>/`
- Worker prompts: `.github/skills/<skill-name>/evals/evals-public.json`
- Hidden grading spec: `.github/skills/<skill-name>/evals/grading-spec.json`
- Result root: `/test/iteration-N/`

## Execution protocol

The run order is mandatory:

1. Move every directory from `.github/skills/` to `test/iteration-N/_disabled-skills/` and write a relocation manifest.
2. Run `python test/scripts/skill_suite_tools.py protocol-preflight --iteration test/iteration-N --workspace-root .` so the active prompt/schema/hook version is frozen into the iteration metadata before scoring begins.
3. Start fresh sessions or fresh workers created **after** the relocation step, with no prior exposure to workspace skill contents.
4. Run **all** eval prompts for **all** skills in `without_skill` mode first, dispatching independent `<skill, run_number>` workers in parallel.
5. Save one English response per eval and write one canonical run-metrics JSON per skill configuration with `skill_suite_tools.py write-run-metrics`.
6. Prefer `n >= 3` repeated runs per `<skill, configuration>` when you want publishable evidence; use `--run-number` during materialization and metrics writing.
7. Run `skill_suite_tools.py normalize-metrics` and `skill_suite_tools.py validate-metrics` on the iteration before building `without_skill` summaries; fix or rerun any configuration that still fails validation.
8. Build one anonymous summary JSON per `without_skill` configuration.
9. Restore every skill directory back into `.github/skills/` and write a restoration manifest.
10. Start fresh sessions or fresh workers created **after** the restore step.
11. For each skill, read `SKILL.md` and `evals/evals-public.json`, then run all eval prompts in `with_skill` mode, again using parallel `<skill, run_number>` workers.
12. Save one English response per eval and write one canonical run-metrics JSON per skill configuration with `skill_suite_tools.py write-run-metrics`.
13. Run `skill_suite_tools.py normalize-metrics` and `skill_suite_tools.py validate-metrics` on the iteration before building `with_skill` summaries; fix or rerun any configuration that still fails validation.
14. Build one anonymous summary JSON per `with_skill` configuration.
15. Blind the pairwise outputs into `A.md` and `B.md` per eval (and per run when repeated runs are enabled).
16. Compare `A` vs `B` without revealing the mapping, using only `grading-spec.json` as hidden scoring input, and parallelize comparator workers across independent `<skill, eval_id, run_number>` tasks. Comparator workers must remain MCP-free.
17. Run `skill_suite_tools.py validate-executable-checks --iteration test/iteration-N --workspace-root .` so LikeC4 snippets get a machine-checked validity signal.
18. Run `skill_suite_tools.py normalize-metrics` and then `skill_suite_tools.py validate-metrics` for the whole iteration; resolve any remaining metric issues before aggregation.
19. Aggregate capability, consumption, executable-validity, and execution-time metrics per skill.
20. Produce suite-level tables for the full iteration.

Optional experimental probe:

- Instead of the strict relocated baseline phase, you may run a separate hook-only baseline probe with `skill-benchmark-baseline-hook-only` to measure whether hooks alone appear sufficient.
- Do **not** treat that probe as a drop-in replacement for the strict relocated baseline.
- Report it separately until repeated runs prove it trustworthy.

## Critical baseline isolation

This step is **non-negotiable**.

- A `without_skill` run is valid only if workspace skills are physically absent from `.github/skills/` for the entire baseline batch.
- Do not rely on “do not read the skill” instructions alone.
- A hook-only baseline probe may be useful diagnostically, but it is not the default validity rule for benchmark reporting.
- Do not mix `without_skill` and `with_skill` workers in the same phase.
- If a baseline response mentions workspace skill names or skill-only handoff patterns that only come from `SKILL.md`, invalidate that baseline batch and rerun it from the physical-disable step.
- Mentioning or using the allowed LikeC4 MCP grounding steps is not, by itself, a baseline contamination signal.
- Keep the disabled skill backup under `test/iteration-N/_disabled-skills/` so the procedure is auditable and reversible.

## Anonymization rules

- Never write absolute paths into saved artifacts.
- When a path must be mentioned, use repository-relative paths only.
- Keep summaries minimal: use eval ids and relative output paths, not raw prompt text.
- Do not emit terminal transcripts, environment dumps, or workspace listings.
- Keep the reporting focused on quality, consumption proxies, and timing.

## Worker isolation protocol

- Run `with_skill` and `without_skill` in separate fresh sessions or fresh workers.
- A worker may handle **one skill and one configuration only**.
- Fresh baseline sessions/workers for `without_skill` must be started only after skills were moved out of `.github/skills/`.
- Fresh skill-enabled sessions/workers for `with_skill` must be started only after skills were restored into `.github/skills/`.
- A `with_skill` worker may read the target `SKILL.md`, its `evals/evals-public.json`, and repository files needed to answer accurately.
- A `with_skill` worker must not read `grading-spec.json`.
- A `without_skill` worker may read repository files needed to answer accurately, but must not read any `SKILL.md` content.
- Do not reuse a worker that has already read a skill file for any `without_skill` task.
- Use parallel waves as the default dispatch mode for each phase; reduce concurrency before falling back to fully serial execution.
- Parallelize across independent workers only when their output directories do not overlap.
- Parallelize **within a phase** (`without_skill` batch or `with_skill` batch), never across both phases at once.

### Custom-agent mapping

When using the workspace benchmark agents, keep this mapping explicit:

- benchmark manager → `skill-benchmark-manager`
- `without_skill` phase → `skill-benchmark-baseline`
- experimental hook-only `without_skill` probe → `skill-benchmark-baseline-hook-only`
- `with_skill` phase → `skill-benchmark-with-skill`
- blind comparison → `skill-blind-comparator`

The manager may delegate only to those constrained benchmark workers.

### Critical subagent propagation rule

- A benchmark worker must not escape its file-access policy through subagents.
- Worker agents should therefore set `agents: []` unless a future helper agent exists with an equal or stricter hook policy.
- If a manager delegates work, it must do so only to explicitly allowlisted benchmark worker agents.
- Do not use unconstrained exploratory or generic subagents anywhere in the measured benchmark flow.
- Do not assume a parent agent's hooks are automatically reused by a delegated custom worker. Each benchmark worker must carry its own read-only tool limits and its own scoped hook policy.

## Isolation rules

### with_skill

- Read the target `SKILL.md` first.
- You may read repository files needed to answer accurately.
- Do not read unrelated skill files unless the target skill explicitly requires a handoff reference.
- Do not use non-LikeC4 MCP tools.
- All LikeC4 MCP tools (`likec4/*`) are allowed for project grounding and repository validation.
- Answer in English only.
- Save outputs only under the assigned `/test/iteration-N/<skill-name>/...` directory.

### without_skill

- Do **not** read any `SKILL.md` file.
- You may read repository files needed to answer accurately.
- Do not use non-LikeC4 MCP tools.
- All LikeC4 MCP tools (`likec4/*`) are allowed for project grounding and repository validation.
- Answer in English only.
- Save outputs only under the assigned `/test/iteration-N/<skill-name>/...` directory.

## Required artifact layout

```text
/test/
  skill-suite-eval-prompt.md
  scripts/
    skill_suite_tools.py
  iteration-N/
    _disabled-skills/
    suite-summary.json
    suite-summary.md
    _meta/
      notes.md
      protocol-lock.json
      skills-relocation.json
      skills-restoration.json
      executable-checks-summary.json
      metric-normalization.json
      metric-validation.json
    <skill-name>/
      with_skill-run-metrics.json
      without_skill-run-metrics.json
      with_skill-executable-checks.json
      without_skill-executable-checks.json
      with_skill-summary.json
      without_skill-summary.json
      blind-comparisons.json
      eval-0/
        with_skill/
          response.md
          run-1/
            response.md
          run-2/
            response.md
        without_skill/
          response.md
        blind/
          A.md
          B.md
          run-2/
            A.md
            B.md
        blind-map.json
        blind-map.run-2.json
      eval-1/
        ...
```

## Expected run-summary schema

Each configuration summary file should use this shape:

```json
{
  "skill_name": "create-element",
  "configuration": "with_skill",
  "language": "English",
  "mcp_used": false,
  "run_count": 3,
  "summary": {
    "elapsed_seconds_total": 12.34,
    "elapsed_seconds_per_eval": 3.09,
    "response_words_total": 731,
    "response_words_per_eval": 182.75,
    "files_read_count": 4,
    "files_written_count": 4
  },
  "variance": {
    "elapsed_seconds_per_eval": {"mean": 3.09, "stddev": 0.41, "min": 2.7, "max": 3.6}
  },
  "runs": [
    {
      "run_number": 1,
      "summary": {
        "elapsed_seconds_total": 12.34,
        "elapsed_seconds_per_eval": 3.09,
        "response_words_total": 731,
        "response_words_per_eval": 182.75,
        "files_read_count": 4,
        "files_written_count": 4
      },
      "evals": [
        {
          "id": 0,
          "run_number": 1,
          "response_path": "eval-0/with_skill/run-1/response.md",
          "response_words": 170
        }
      ]
    }
  ],
  "evals": [
    {
      "id": 0,
      "run_number": 1,
      "response_path": "eval-0/with_skill/response.md",
      "response_words": 170
    }
  ]
}
```

All metric fields shown above are required when available in the schema; do not emit `null` for `elapsed_seconds_total`, `files_read_count`, or `files_written_count`.

Each configuration must also write a compact run-metrics file:

```json
{
  "skill_name": "create-element",
  "configuration": "with_skill",
  "language": "English",
  "mcp_used": false,
  "started_at": "2026-03-12T10:00:00Z",
  "finished_at": "2026-03-12T10:00:12Z",
  "elapsed_seconds_total": 12.34,
  "files_read_count": 4,
  "files_written_count": 4,
  "run_number": 1
}
```

Required rule: every key in the run-metrics schema above must be present and non-null.

Recommended safe path: write the file with the helper instead of typing JSON manually.

```bash
python test/scripts/skill_suite_tools.py write-run-metrics \
  --output test/iteration-3/create-element/with_skill-run-metrics.json \
  --started-at 2026-03-12T10:00:00Z \
  --finished-at 2026-03-12T10:00:12Z \
  --files-read-count 4 \
  --files-written-count 5
```

This command infers `skill_name` and `configuration` from the output path when possible and always writes the canonical schema expected by summary/validation.

After a batch, run:

```bash
python test/scripts/skill_suite_tools.py normalize-metrics --iteration test/iteration-3
python test/scripts/skill_suite_tools.py validate-metrics --iteration test/iteration-3
```

`normalize-metrics` repairs known legacy alias keys in-place before validation. `validate-metrics` must still end with zero remaining issues.

## Blind-comparison rules

For each eval:

- Randomize whether `A` is `with_skill` or `without_skill`.
- Save the mapping in `blind-map.json`.
- The blind comparator must read only `A.md`, `B.md`, and the hidden `grading-spec.json` entry for that eval.
- The blind comparator must not use MCP tools, including LikeC4 MCP.
- The comparator must not inspect any file that reveals the real configuration.

### Expected comparison schema

```json
{
  "skill_name": "create-element",
  "comparisons": [
    {
      "schema_version": 2,
      "eval_id": 0,
      "run_number": 1,
      "winner": "A",
      "reasoning": "A is more complete and repo-aligned.",
      "rubric": {
        "A": {"content_score": 9.0, "structure_score": 8.5, "overall_score": 8.8},
        "B": {"content_score": 6.0, "structure_score": 6.5, "overall_score": 6.2}
      },
      "expectation_results": {
        "A": {"passed": 4, "total": 4, "pass_rate": 1.0},
        "B": {"passed": 2, "total": 4, "pass_rate": 0.5}
      }
    }
  ]
}
```

## Metric definitions

### Capability

Capture capability with:

- blind win rate
- expectation pass rate
- blind-comparator rubric score

### Consumption

Capture consumption with directly observed proxies:

- response words per eval
- files read count
- files written count

Do **not** invent token counts if they are unavailable.

### Execution time

Capture wall-clock seconds per configuration and per eval.

## Metric legend

Use this legend in reports and reviewer notes so readers interpret the metrics consistently.

| Metric | Meaning | How to read it |
| --- | --- | --- |
| `with-skill blind win rate` | Share of blind comparisons won by the `with_skill` response. | Higher is better for the skill. A tie is not a win. |
| `expectation pass rate` | Average share of listed expectations satisfied by a response. | Higher is better. `expectation delta = with_skill - without_skill`. |
| `rubric score` | Blind comparator overall quality score on a 0–10 scale. | Higher is better. `rubric delta = with_skill - without_skill`. |
| `time per eval` | Average wall-clock seconds spent per eval. | Lower is faster. `time delta = with_skill - without_skill`, so a negative delta means the skill was faster. |
| `response words per eval` | Average response length in words. | Lower means more concise, but not automatically better unless quality is preserved. |
| `files read count` | Count of repository files intentionally read during a run. | Proxy for context consumption. Higher means the run consumed more repository context. |
| `files written count` | Count of files written under `/test` for a run. | Mostly an auditability/procedure metric, not a quality metric. |
| `executable validity` | Share of snippet-bearing eval runs whose LikeC4 snippets pass automated structural checks. | Higher is better. `executable delta = with_skill - without_skill`. |

### Reading deltas correctly

- `expectation delta > 0` means `with_skill` satisfied more expected criteria.
- `rubric delta > 0` means `with_skill` was judged better overall.
- `time delta < 0` means `with_skill` was faster.
- `words delta < 0` means `with_skill` was more concise.
- `files read delta > 0` means `with_skill` consumed more repository context.
- `executable delta > 0` means `with_skill` produced more structurally valid LikeC4 snippets.

Do not treat consumption metrics as quality metrics on their own. A shorter answer or fewer files read is only better if capability remains strong.

## Final reporting requirements

Produce at least these tables in `suite-summary.md`:

1. **Suite overview**
   - skill
   - eval count
  - run count
   - with-skill blind win rate
   - expectation delta
   - rubric delta
   - time per eval delta
  - executable delta
   - response words per eval delta
   - files read delta
  - high-variance eval count

2. **Per-skill detailed comparison**
   - with_skill vs without_skill capability metrics
  - with_skill vs without_skill executable validity metrics
   - with_skill vs without_skill consumption metrics
   - with_skill vs without_skill time metrics

3. **High-variance evals**
  - skill
  - source (`with_skill`, `without_skill`, or `blind`)
  - eval id
  - run count
  - whether blind winners flipped across runs

4. **Previous-iteration comparison** (if available)
   - current vs previous blind win rate
   - current vs previous expectation delta
   - current vs previous quality delta
   - current vs previous time delta

If no previous iteration exists, state that explicitly.

## Recommended evaluator wording

When running a benchmark subtask, prefer an instruction bundle like this:

- answer in English only
- if you are a scored `with_skill` / `without_skill` worker, do not use non-LikeC4 MCP tools
- if you are the benchmark manager or blind comparator, do not use MCP tools at all
- do not edit repository source files
- save outputs only under `/test/iteration-N/...`
- keep the answer focused on the eval prompt
- avoid extra narration outside the requested artifact
- keep logs anonymous and never emit absolute workspace paths
- do not read any other skill file than the target one in `with_skill`
- do not read any `SKILL.md` in `without_skill`
- baseline phase: confirm that `.github/skills/` was physically emptied into `test/iteration-N/_disabled-skills/` before answering
- skill phase: confirm that `.github/skills/` was restored before answering

## Success condition

The iteration is complete when:

- every skill with split eval artifacts has both configurations executed
- every eval has a blind comparison
- `test/iteration-N/_meta/protocol-lock.json` exists
- `test/iteration-N/_meta/executable-checks-summary.json` exists
- `test/iteration-N/_meta/metric-normalization.json` exists (or `normalize-metrics` was run without needing changes)
- `test/iteration-N/_meta/metric-validation.json` exists and reports no remaining metric issues
- `/test/iteration-N/suite-summary.{json,md}` exists
- the suite report includes previous-iteration comparison if available
