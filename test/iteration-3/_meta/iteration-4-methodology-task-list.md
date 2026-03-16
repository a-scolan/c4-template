# Iteration 4 Methodology Task List

## Goal

Turn the iteration-3 critique into a tighter benchmark protocol: narrower worker context, less benchmark leakage, more reproducible judging, and stronger evidence.

## Status update — 2026-03-13

All five methodology items below have now been implemented on this branch:

- **M01**: workers use `evals-public.json`, blind/grading flows use `grading-spec.json`, and hooks block hidden grading artefacts from `with_skill` workers.
- **M02**: comparator materialization now validates a fixed schema with a mandatory 0–10 rubric scale and explicit expectation counts.
- **M03**: the benchmark protocol is versioned via `test/benchmark-protocol.json`, and `protocol-preflight` writes `test/iteration-N/_meta/protocol-lock.json` before scored runs.
- **M04**: the harness now supports repeated runs with `--run-number`, run-aware blind artefacts, variance reporting, and high-variance eval surfacing.
- **M05**: automated LikeC4 executable checks are written per configuration and rolled into suite aggregation as a separate validity dimension.

## Scope note

The worker read policy has already been tightened on this branch so that scored workers may consult only `projects/shared/` outside the locked skill. The tasks below cover the next methodological step-change before running `iteration-4`.

## Prioritization

- **P0**: required before trusting a new broad benchmark campaign
- **P1**: strong evidence upgrades that should follow immediately after P0

## Summary

| ID | Priority | Task | Expected outcome |
| --- | --- | --- | --- |
| M01 | P0 | Separate prompt and grading artefacts | Workers can no longer read the scoring rubric directly |
| M02 | P0 | Normalize comparator outputs | Blind results become schema-stable and cross-skill comparable |
| M03 | P0 | Freeze the benchmark protocol | Campaigns become rerunnable without prompt drift mid-run |
| M04 | P1 | Add repeated runs with variance | Reported gains become statistically more credible |
| M05 | P1 | Add executable LikeC4 checks | Benchmark quality stops relying on text quality alone |

## Detailed tasks

### M01 — Separate prompt and grading artefacts

**Why**
- Workers currently read `evals.json`, which exposes not only the prompt but also `expected_output` and `expectations`.
- This encourages teaching to the test and inflates expectation pass rates.

**Actions**
- Introduce `evals-public.json` for worker execution with prompt-only data plus any necessary input files.
- Introduce `grading-spec.json` for comparator/grading only, containing `expected_output`, expectations, and any hidden rubric hints.
- Update helper scripts so workers never need the grading file.
- Update blind comparator bundles so they receive the grading spec without seeing any mapping artefact.

**Definition of done**
- Worker prompts and materialization flow use `evals-public.json` only.
- Comparator/grading flow uses `grading-spec.json` only.
- Policy tests fail if a worker attempts to read the hidden grading artefact.

### M02 — Normalize comparator outputs

**Why**
- Comparator outputs currently mix scales (`0–1`, `0–5`, `0–10`-ish) and optional fields.
- Suite-level rubric aggregation is therefore weaker than it looks.

**Actions**
- Define one required comparator schema.
- Force `overall_score` onto a fixed `0–10` scale.
- Standardize `winner`, `reasoning`, `rubric`, and `expectation_results` fields.
- Add an automatic schema-validation step before `materialize-comparisons` accepts a payload.

**Definition of done**
- Every blind payload validates against one schema.
- Aggregation no longer mixes incompatible rubric scales.
- Comparator reruns fail fast on malformed or partial JSON.

### M03 — Freeze the benchmark protocol

**Why**
- A campaign should be run-or-fail, not adjusted mid-flight.
- Prompt drift, schema drift, or comparator-prompt drift weakens comparability.

**Actions**
- Freeze the worker prompt template for `baseline`, `with_skill`, and `blind_compare` before the run.
- Freeze the raw payload schema for workers and comparators.
- Add a preflight check that aborts the campaign if expected protocol files or prompts differ from the declared version.
- Record the protocol version in iteration metadata.

**Definition of done**
- `iteration-4` has a declared protocol version.
- A mismatched prompt/schema aborts the run before scoring begins.
- Post-hoc reconstruction of the exact prompts is possible from committed artefacts.

### M04 — Run each eval at least 3 times per configuration

**Why**
- Single-run outcomes are directional, not robust.
- Small deltas are hard to trust without variance.

**Actions**
- Run each eval `n >= 3` times per config, ideally `3–5`.
- Extend metrics aggregation to report mean, spread, and outliers by config and by eval.
- Keep blind comparison grouping stable so repeated runs remain auditable.

**Definition of done**
- Suite summaries report mean plus variance for win rate / expectation pass rate / timing.
- High-variance evals are surfaced explicitly.
- A single lucky run can no longer dominate the headline claim.

### M05 — Add executable LikeC4 checks

**Why**
- Blind text quality is useful, but it is not the same as executable correctness.
- For LikeC4, parse/render validity matters.

**Actions**
- Add parse/render checks for generated LikeC4 snippets where feasible.
- Add validation for element refs, kinds, and relationships.
- Add smoke checks for view renderability or minimally valid structure when a response includes concrete snippets.
- Feed these checks into grading or as a separate validation dimension.

**Definition of done**
- At least one executable check exists for snippet-bearing evals.
- Factual but non-renderable answers no longer score as fully correct.
- Benchmark summaries distinguish textual quality from executable validity.