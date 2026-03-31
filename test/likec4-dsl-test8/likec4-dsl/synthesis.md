# Skill Synthesis — `likec4-dsl` | Iteration: likec4-dsl-test8

Generated: 2026-03-31 | Runs: 2 per eval | Evals: 32

---

## 1. Quantitative summary

| Metric | With skill | Without skill | Δ |
|---|---|---|---|
| Blind win rate | 76.6% (49 wins) | 12.5% (8 wins) | +64.1 pp |
| Ties | 7 (10.9%) | — | — |
| Expectation pass rate | 0.951 | 0.737 | **+0.214** |
| Rubric score (0–10) | 9.30 | 7.17 | **+2.13** |
| Seconds / eval | 13.40 s | 20.00 s | **−6.60 s** |
| Words / eval | 66.4 | 80.6 | **−14.2** |
| Files read / eval | 32.0 | 32.0 | 0 |
| Executable validity | 65.3% | 58.7% | **+6.6 pp** |

**Verdict: strong positive signal.** The skill keeps the same blind win rate as the previous campaign’s headline result, but this time it is also faster, shorter, and modestly better on executable validity.

---

## 2. Per-eval breakdown (blind comparison outcomes)

| Eval | Outcomes | Flips? | Topic | Key discriminator |
|---|---|---|---|---|
| 0 | with_skill | no | File-scoped validate | Exact `validate --json --no-layout --file` semantics + filtered fields |
| 1 | with_skill | no | Minimal config JSON | `$schema` + nearest-config scope explanation |
| 2 | with_skill | no | PNG export command | Better `export png` flag shape and filter usage |
| 3 | with_skill | no | Dynamic sequence view | `dynamic view` + `variant sequence` + backward response arrows |
| 4 | with_skill / without_skill | yes | View-local styling | Very small formatting/minimalism difference only |
| 5 | with_skill | no | Named deployment instances | Self-contained `deployment { vm ... }` shape mattered |
| 6 | with_skill | no | `_`, `*`, `**` predicates | Correct relationship-qualified meaning for `**` |
| 7 | with_skill | no | Inherited scope via `extends` | Exact inbound predicate form won |
| 8 | with_skill | no | Reusable predicate groups | Canonical `global { predicateGroup ... }` syntax |
| 9 | with_skill | no | Chained dynamic hop | Single `parallel { ... }` block + proper hop body attachment |
| 10 | with_skill | no | Cumulative deployment-tag fixture | Correct one-file fixture and logical-vs-deployment shape |
| 11 | with_skill | no | `extend` metadata merge | Correct duplicate metadata merge-into-array explanation |
| 12 | without_skill | no | Deployment-view limitations | Unsupported `include * with {}` / `global style` handling |
| 13 | with_skill | no | Body tag ordering | `#tag` before property inside block body |
| 14 | with_skill | no | Invalid top-level `styles` | Correct allowed top-level block list |
| 15 | with_skill | no | Identifier validity | `payment-api` valid, `payment.api` invalid |
| 16 | TIE / with_skill | yes | Parent-child relationship misuse | Repair pattern close; one run tied |
| 17 | without_skill | no | Cross-file FQN resolution | Slight edge on lexical-scope / import-non-solution framing |
| 18 | with_skill / without_skill | yes | Async relationship extend identity | Source/target/title/kind explanation varied by run |
| 19 | with_skill | no | Scoped `include *` semantics | Direct-children base set, not recursive subtree |
| 20 | with_skill | no | Multi-file validate CLI | Exact repeated `--file` invariants |
| 21 | with_skill | no | Valid inherited-scope view | Minimal `include -> cloud.backend` answer |
| 22 | with_skill / without_skill | yes | Chained dynamic expression | Continuation-line vs single-line chain disagreement |
| 23 | TIE | no | Deployment tag inheritance | Both stable on cumulative-tag semantics |
| 24 | with_skill | no | Async matcher correction | Metadata-bearing `extend` block helped |
| 25 | with_skill | no | `filteredFiles = 2` interpretation | Better tri-file validate explanation |
| 26 | with_skill | no | PredicateGroup precision | Exact `global predicate core-services` form |
| 27 | with_skill / without_skill | yes | Scoped incoming relationships | `include ->` vs `include * ->` remained ambiguous |
| 28 | TIE / with_skill | yes | Exact unkinded-extend rejection | One run tied, one favored stricter ambiguity wording |
| 29 | TIE / with_skill | yes | Multiple-choice chained-step answer | One run tied on equally acceptable explanation detail |
| 30 | TIE | no | Exact tag filter matrix | Both stable and equivalent |
| 31 | with_skill | no | Matcher classification triage | Correctly labeling option (3) as wrong |

**Disagreements to verify:** 4, 16, 18, 22, 27, 28, 29. These are benchmark-hardening candidates before they are treated as real skill regressions.

---

## 3. Executable validity detail

| Config | Applicable runs | Valid rate |
|---|---|---|
| with_skill | 49 | 65.3% |
| without_skill | 46 | 58.7% |

Δ = **+6.6 pp** in favor of the skill.

Important caveat: the executable checker still appears partially misaligned with the DSL under test. It flags several core constructs as unknown (`service`, `system`, `container`, `component`, `instanceOf`) and also rejects some dynamic-step forms with `Unknown relationship kind '->'`. So this metric is directionally useful, but not yet a clean parser-truth proxy.

---

## 4. High-variance eval analysis

19 of 32 evals were flagged high-variance overall, but only a smaller subset show meaningful winner instability.

Most important patterns:

- **Stable strong wins**: exact CLI syntax and exact DSL-shape tasks remain reliable wins for the skill (`0`, `1`, `2`, `9`, `10`, `14`, `20`, `25`, `31`).
- **Stable weak spots**: eval `12` (deployment-view unsupported constructs) and eval `17` (cross-file FQN explanation precision) are the only clear non-flip areas where the skill still trails.
- **Ambiguous pockets**: evals `16`, `18`, `22`, `27`, `28`, `29` show wording- or canonical-form sensitivity rather than a broad capability gap.

The biggest true miss remains **eval 12**, where the without-skill answer consistently handled the “unsupported in deployment views” distinction better.

---

## 5. Comparison with previous iteration (likec4-dsl-test7)

| Metric | test7 | test8 | Δ |
|---|---|---|---|
| Win rate | 76.6% | 76.6% | 0.0 pp |
| Expectation Δ | 0.251 | 0.214 | −0.037 |
| Rubric Δ | 2.31 | 2.13 | −0.18 |
| Time Δ / eval | +1.46 s | **−6.60 s** | **−8.06 s** |
| Executable Δ | −0.9 pp | **+6.6 pp** | **+7.5 pp** |

Headline read: blind quality stayed essentially flat at the top level, while efficiency improved dramatically and executable validity moved from slightly negative to modestly positive. The small drop in expectation/rubric deltas is worth watching, but it is not large enough to outweigh the speed and validity gains.

---

## 6. Errors and issues for future benchmark improvements

1. **`materialize-comparisons` CLI mismatch**  
   The command rejects `--workspace-root`, but that mistake is easy to make during recovery. The workflow docs / manager prompts should state the exact accepted argument shape more explicitly.

2. **Blind comparator ack schema inconsistency**  
   Comparator workers returned mixed ack shapes (`status`, `winner`, `raw_json_path`, `raw_output_path`, sometimes only a subset). The raw JSON journals were authoritative, but the ack contract should be normalized.

3. **Allowlist friction for harmless inspection**  
   During the campaign, several grouped-command or inspection attempts were denied even though they were operationally benign. The benchmark manager docs should document the exact allowed command patterns more clearly.

4. **Hook-audit availability ambiguity**  
   Earlier validation hit a missing hook-audit artifact. The tooling should emit a clearer “audit not enabled / no file expected” state instead of making this look like a possible failure.

5. **Worker-noise anomalies should be tracked explicitly**  
   Earlier phases saw restricted directory-listing attempts and one duplicate baseline ack. These were non-fatal, but they should be logged in a structured “harness noise” bucket.

6. **Executable checker lags current DSL reality**  
   The checker still rejects real LikeC4 constructs such as `service`, `system`, `container`, `component`, `instanceOf`, and some dynamic arrow forms. This depresses validity rates and can blur benchmark conclusions.

7. **Snippet extraction is too brittle on prose-heavy answers**  
   Some runs produced brace-only fragments or split multi-block snippets (notably around evals `1`, `10`, and `26`). The executable-validation extractor should prefer fenced blocks and avoid orphan brace fragments.

8. **Cross-contamination check result: clean**  
   On the positive side, `validate-blind-isolation` passed with zero issues, so there is no evidence of cross-iteration / cross-run contamination in this iteration.

---

## 7. Skill improvement recommendations (Anthropic best-practices pass)

| Check | Finding |
|---|---|
| Concision / token economy | Good. The skill is **shorter** than baseline by 14.2 words/eval while still winning strongly. No obvious instruction bloat. |
| Degrees of freedom fit | Mostly good, but still slightly under-constrained on “choose the exact canonical form” tasks (evals `12`, `16`, `18`, `22`, `27`, `28`, `29`). |
| Triggerability metadata | Looks healthy in practice: no evidence of under-triggering or spurious overhead in this campaign. |
| Progressive disclosure | Strong. The skill seems to help exact DSL/CLI tasks without causing longer answers or extra file reads. |
| Workflow + feedback loop | Strong on command-first and contrastive explanations; this clearly helped evals `0`, `20`, `25`, and `31`. |
| Anti-pattern scan | Keep reinforcing exact matcher identity, unsupported deployment-view syntax, and canonical predicateGroup forms. |

Concrete rewrites worth considering:

- Add one explicit **“unsupported in deployment views”** mini-table contrasting local `style` vs unsupported `include * with {}` / `global style`.
- Add one tighter **relationship-matcher triage** example: correct vs ambiguous vs wrong when async/sync typed alternatives coexist.
- Add one short **cross-file FQN** reminder that lexical/container scope does not carry across files, even when include/imports are present.
- Preserve the current concise style; the benchmark says the skill is already winning without verbosity.
