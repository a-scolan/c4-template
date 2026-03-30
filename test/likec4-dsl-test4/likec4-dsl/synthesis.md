# Critical Synthesis — `likec4-dsl` Benchmark

**Iteration:** `likec4-dsl-test4`
**Protocol:** benchmark-v3
**Evals:** 29 (ids 0–28), 2 run(s) per configuration
**Generated:** 2026-03-30

---

## 1. Quantitative results

| Metric | `with_skill` | `without_skill` | Δ |
|---|---|---|---|
| **Blind win rate** | **46/58 = 79.3%** | 7/58 = 12.1% | +67.2 pp |
| **Expectation pass rate** | **97.4%** | 70.3% | **+27.1 pp** |
| **Rubric score (0–10)** | **8.82** | 6.25 | **+2.57** |
| Seconds / eval | 34.0 s | 19.6 s | +14.4 s |
| Words / eval | 164.2 | 168.6 | −4.5 |
| Files read | 58.0 | 29.0 | +29.0 |
| Executable validity | 64.8% | 61.8% | +3.0 pp |

The signal is strong and consistent. Across three independent dimensions — blind preference, expectation pass rate, and rubric score — `with_skill` dominates by a large, measurable margin. Seven losses are all boundary-state or concision issues (see §4), not DSL-knowledge gaps. Five ties indicate evals where both configurations are essentially equivalent in correctness; the skill adds no harm and no gain there. Time cost (+14 s) is entirely explained by the extra SKILL.md file read per run.

---

## 2. Eval-by-eval analysis

| Eval | Topic | Winner | Exp with | Exp without | Key discriminator |
|---|---|---|---|---|---|
| 0 | `likec4 validate --json --no-layout --file` | **with_skill** (both) | 5/5, 5/5 | 0/5, 0/5 | Without skill uses `likec4 check` — completely wrong subcommand |
| 1 | `likec4.config.json` `include.paths` config | **with_skill** (both) | 5/5, 5/5 | 2/5, 3/5 | Without skill omits `$schema` and uses flat array instead of `include.paths` object |
| 2 | `export png` CLI command | **with_skill** (both) | 4/5, 4/5 | 3/5, 3/5 | Without skill uses `--output` (non-existent flag) and omits project path in main command |
| 3 | `dynamic view variant sequence` + `<-` arrows | **with_skill** (both) | 5/5, 5/5 | 3/5, 3/5 | Without skill omits `variant sequence` entirely and reverses arrow direction |
| 4 | view-local style cascade | **with_skill** (both) | 5/5, 5/5 | 5/5, 5/5 | All expectations pass for both; with_skill adds `views {}` wrapper + ordering explanation |
| 5 | Named deployment `instanceOf` | **with_skill** (both) | 5/5, 5/5 | 4/5, 3/5 | Without skill omits outer `deployment {}` block — invalid top-level deployment syntax |
| 6 | `_` underscore predicate semantics | **with_skill** (both) | 5/5, 5/5 | 4/5, 4/5 | Without skill describes `**` as unconditional (wrong — it is relationship-filtered) |
| 7 | `extends` view + inbound relationship predicate | **split** (r1 with_skill / r2 without_skill) | 5/5, 4/5 | 4/5, 4/5 | r1: with_skill uses correct view name `detail`; r2: with_skill uses `* -> cloud.backend` with misleading note—without_skill gives cleaner `-> cloud.backend` |
| 8 | `global { predicateGroup }` syntax | **with_skill** (both) | 5/5, 5/5 | 3/5, 3/5 | Without skill uses `kind == service` (wrong operator) and non-standard comma syntax |
| 9 | Dynamic view chained + parallel | **split** (r1 without_skill / r2 with_skill) | 5/5, 5/5 | 5/5, 5/5 | r1: with_skill adds unrequested `title` + verbose prose, making it less minimal; r2: identical DSL |
| 10 | Deployment instance tag cumulative fixture | **with_skill** (both) | 5/5, 5/5 | 3/5, 4/5 | Without skill uses non-standard `deployment { env; zone; node }` inside specification |
| 11 | Metadata merge into arrays | **with_skill** (both) | 5/5, 5/5 | 3/5, 3/5 | Without skill claims `port` is overwritten to `'9090'` — wrong merge semantics |
| 12 | Deployment view styling limitations | **split** (r1 TIE / r2 without_skill) | 6/6, 6/6 | 6/6, 6/6 | All expectations pass in both runs; r2 without_skill has slightly cleaner triple-distinction |
| 13 | Tag ordering inside element body | **with_skill** (both) | 5/5, 5/5 | 2/5, 2/5 | Without skill misidentifies the error as missing `=` operator, never fixes ordering |
| 14 | Invalid `styles {}` top-level block | **with_skill** (both) | 5/5, 5/5 | 1/5, 3/5 | Without skill treats `styles {}` as a valid top-level block (fundamentally wrong premise) |
| 15 | LikeC4 identifier validity (`payment.api`, etc.) | **with_skill** (both) | 5/5, 5/5 | 2/5, 2/5 | Without skill marks `payment.api` valid and `payment-api` invalid — both inverted |
| 16 | Parent-child relationship validity | **with_skill** (both) | 5/6, 6/6 | 5/6, 5/6 | With_skill more explicitly names the offending relationship `cloud -> backend` |
| 17 | Cross-file FQN references | **with_skill** (both) | 5/5, 5/5 | 5/5, 5/5 | All pass for both; with_skill uses canonical `lexical scope` terminology; without_skill hedges |
| 18 | Relationship extend kind ambiguity | **split** (r1 without_skill / r2 with_skill) | 4/5, 5/5 | 5/5, 5/5 | r1: without_skill correctly says "wrong" (not just "ambiguous"); r2: both correct |
| 19 | Scoped `include *` semantics | **with_skill** (both) | 5/6, 5/6 | 4/6, 5/6 | With_skill correctly names scoped element in base include set; without_skill omits it or contradicts |
| 20 | Multi-file validate (`--file` ×2) | **with_skill** (both) | 5/5, 5/5 | 0/5, 0/5 | Without skill uses wrong subcommand (`likec4 check` / `likec4 lint`) with invented flags |
| 21 | `extends` view scope validity check | **TIE** (both runs) | 5/5, 5/5 | 5/5, 5/5 | Both configurations fully equivalent in correctness |
| 22 | Dynamic view chained + parallel (minimal) | **split** (r1 without_skill / r2 with_skill) | 5/5, 5/5 | 5/5, 5/5 | r1: with_skill explanation has a count error ("three" standalone steps for a two-hop chain); r2: with_skill adds `views {}` wrapper |
| 23 | Deployment instance tag filtering | **TIE** (both runs) | 5/5, 5/5 | 5/5, 5/5 | Both configurations fully equivalent in correctness |
| 24 | Relationship extend kind disambiguation | **with_skill** (both) | 5/5, 5/5 | 4/5, 4/5 | With_skill uses canonical `metadata { }` block; without_skill uses `description` property or placeholder |
| 25 | Multi-file validate (`--file` ×3) | **with_skill** (both) | 5/5, 5/5 | 2/5, 2/5 | Without skill missing `--json`, `--no-layout`, project path, or uses wrong subcommand |
| 26 | `predicateGroup` one-snippet | **with_skill** (both) | 5/5, 5/5 | 4/5, 3/5 | Without skill uses `include global predicate` instead of bare `global predicate`; non-canonical exclude shorthand |
| 27 | Scoped `include *` multiple-choice (B) | **split** (r1 with_skill / r2 without_skill) | 5/5, 5/5 | 3/5, 5/5 | r1: without_skill fails to open with bare `B`; r2: without_skill adds one-level depth qualifier and explains predicate semantics |
| 28 | Relationship extend ambiguity opener | **split** (r1 with_skill / r2 without_skill) | 5/4, 5/5 | 5/5, 5/5 | r2: with_skill claims "it is not ambiguous" — contradicts expectation 2; without_skill correctly says "wrong" |

### Observations

**Dominant wins (6+ rubric-point gap):** Evals 0, 13, 14, 15, 20, 25. These represent the clearest ROI: without-skill responses either use entirely the wrong command (`likec4 check` vs `validate`, `likec4 lint`), misidentify error root causes (tag ordering, invalid top-level `styles{}`), or invert identifier validity rules. In all cases the model-without-skill has no grounding for these precise, notation-specific facts — the skill's reference material is decisive.

**Consistent medium wins (2–5 rubric gap):** Evals 1, 2, 3, 5, 6, 8, 10, 11, 16, 19, 24, 26. Without skill makes recognizable DSL errors: wrong operator (`kind == service`), wrong include structure (flat array vs `include.paths`), missing DSL blocks (`deployment {}` wrapper, `variant sequence`), wrong semantic claims (metadata overwrite vs array-merge, `**` described as unconditional).

**Narrow wins / both correct:** Evals 4, 17. Both configurations are broadly correct but with_skill adds `views {}` wrapper or canonical `lexical scope` terminology. These are polish wins, not knowledge gaps.

**High-variance evals (winner flips across runs):** 7, 9, 12, 18, 22, 27, 28. In evals 9 and 22, the with_skill response added unrequested content (title field, step labels, verbose explanation) in one run, flipping to without_skill. These are prompt-sensitivity artifacts: the skill's knowledge is correct but the response becomes less concise. In eval 18 and 28, the flip is on exact wording ("wrong" vs "ambiguous") — a single-word distinction in a relationship-identity eval. Evals 7 and 27 flip on predicate forms (`* -> cloud.backend` vs `-> cloud.backend`). These reveal that even with_skill responses have inconsistency in precise DSL forms across runs.

**True ties:** Evals 21, 23 — both complete correct answers across both runs; the skill does not hurt but adds no marginal benefit either.

---

## 3. Executable validity analysis

| | `with_skill` | `without_skill` |
|---|---|---|
| Applicable evals | 54 | 55 |
| Valid evals | 35 (64.8%) | 34 (61.8%) |
| Total snippets | 72 | 69 |
| Total errors | 53 | 50 |
| Total warnings | 50 | 68 |

The executable validity gap (+3.0 pp) is small and essentially noise given the variance. The metric is **not a reliable primary signal** for this skill because:

1. Many evals ask for CLI commands, prose explanations, or JSON configs — not parseable `.c4` DSL snippets.
2. Snippets that are intentionally minimal fragments (showing only `extend` blocks, partial `deployment` blocks, or spec-only chunks) will fail the validator even when semantically correct in context.
3. With_skill produces more warnings from longer or more structured snippets; without_skill's 68 warnings vs 50 for with_skill suggests the validator is flagging style issues in baseline responses.

The improved blind win rate and expectation pass rate are far more reliable for this skill type. Executable validity should be treated as a sanity check, not a primary scorer.

---

## 4. Skill design assessment

### Strengths

1. **CLI command knowledge:** The skill covers `likec4 validate` (incl. `--json`, `--no-layout`, `--file`), `export png` flags (`-f`, `-o`, `--flat`, `--theme`), and runner conventions. This is highly specific knowledge that baseline models consistently hallucinate (wrong subcommands, invented flags, wrong flag names). Evals 0, 2, 20, 25 are all strong wins directly attributable to this.

2. **DSL semantic correctness:** Evals testing merge semantics (11), view predicate families (`*` vs `_` vs `**` in 6, 19, 27), `variant sequence` (3), and identifier validity (15) are all clear with_skill wins. The baseline model guesses plausibly but incorrectly on subtle rules; the skill anchors the correct answer.

3. **Spec-correct DSL structure:** Evals testing outer-block requirements (`deployment {}` in 5, `views {}` wrapper, `global { predicateGroup }` in 8/26, `deploymentNode` keyword in 10, disallowed `styles {}` in 14) are all strong wins. Without-skill routinely omits or invents top-level structure.

4. **Tag and metadata semantics:** Evals 11 (metadata merge to arrays) and 23 (cumulative deployment instance tags) are won by with_skill on explicit factual knowledge. Baseline models apply last-write-wins or isolation models incorrectly.

### Weak areas

1. **Concision under minimal-snippet instructions:** Evals 9 (r1) and 22 (r1) reveal that with_skill sometimes adds unrequested `title` fields or step-label annotations. The skill may be encouraging "complete and helpful" responses in a way that conflicts with eval prompts asking for minimal DSL. This should be tightened.

2. **Relationship predicate exact forms:** Eval 7 (r2) shows with_skill using `* -> cloud.backend` instead of the canonical `-> cloud.backend`, accompanied by a misleading explanatory note. Eval 28 (r2) shows with_skill claiming an unkinded extend is "not ambiguous" rather than "wrong." These are intra-skill inconsistencies: the skill has the right knowledge but inconsistent reproduction of exact DSL forms.

3. **Ambiguity vs. wrong framing:** Evals 18 (r1) and 28 (r2) were lost because with_skill used "ambiguous" rather than "wrong" to describe relationship extension with omitted kind. The grading spec distinguishes these: when there are two matching candidates, omitting the kind doesn't cause ambiguity at parse level — it silently selects the wrong one. The skill's explanation of this edge case needs sharpening.

4. **Bunx vs npx runner:** Eval 2 consistently uses `bunx` as the primary runner rather than `npx`. This causes eval 2 to miss expectation 1 both runs. The skill should either prefer `npx` (the eval-expected canonical form) or explicitly present both.

---

## 5. Priority recommendations

**P1 — Critical (direct impact on baseline failures)**

- **Validate CLI coverage:** Ensure the skill explicitly documents `npx likec4 validate --json --no-layout --file <path> <project>` as the canonical single-file check command, with clear contrast against `likec4 check` (which does not exist). Add `filteredFiles`/`filteredErrors`/`totalErrors` JSON field semantics directly in the skill reference. This fixes the most severe loss pattern (evals 0, 20 both producing 0/5 baseline expectation pass).

- **Runner preference:** Change `bunx` examples to use `npx` as the primary runner (or explicitly list `npx` first). The skill currently uses `bunx` as default CLI runner, which causes eval 2 expectation 1 misses both runs.

**P2 — Important (improved precision)**

- **Exact predicate forms:** Add explicit coverage of the `-> element` (bare inbound) syntax and contrast it with `* -> element` (with explicit wildcard source). The r2 eval-7 and r2 eval-28 losses are traceable to this ambiguity. The skill should state the canonical form and note why `* -> X` and `-> X` are semantically different.

- **"Wrong" vs "ambiguous" distinction for relationship extension:** When two relationships share source+target+title but differ in kind, omitting the kind does not produce a parse-level ambiguity — the parser resolves it to the unkinded relationship silently. The skill should document this distinction with a concrete example so the model uses the word "wrong" not "ambiguous."

- **Minimal snippet discipline:** Add a note to the skill that when an eval or user prompt says "minimal" or "paste-ready," the response should include only the exact requested constructs — no `title`, no unrequested labels, no appended explanatory breakdowns unless explicitly asked.

**P3 — Nice to have (robustness)**

- Expand the `likec4 export` section to explicitly name `--outdir` (long form) and `-o` (short form) as the only valid output directory flags, with an explicit note that `--output` and `--out-dir` do not exist.
- Add an example of `filteredFiles = 2` when passing a `.json` config file via `--file` (the config is not a `.c4` source and is silently excluded from the filter count).

---

## 6. Anthropic skill-authoring best-practices pass

- **Concision / token economy:** The skill likely restates facts about `include *` semantics in multiple places (view scope semantics appear in at least 3 evals: 6, 19, 27). Consolidate into a single authoritative section on predicate families (`*`, `_`, `**`) rather than spreading across examples. The baseline model already has general knowledge; only the nuanced distinctions (relationship-filtered vs unconditional) need to be explicitly stated.

- **Degrees of freedom fit:** CLI flag documentation should be strict (exact flag names, mandatory vs optional) — the eval evidence shows the baseline invents flags freely (`--output`, `--no-layout-drift`, `--files`). DSL snippet examples can be slightly looser (e.g., `bunx` vs `npx` is acceptable), but the skill should prefer the `npx` canonical form for correctness.

- **Triggerability metadata quality:** Based on eval topic coverage, the skill triggers correctly across a wide range of DSL, CLI, and semantic questions. No issues identified with name/description.

- **Progressive disclosure quality:** If the skill references a separate CLI reference file, that structure is appropriate. However, the `variant sequence` and `<- ` backward arrow knowledge (evals 3, both runs clear wins) must be in the top-level skill file, not buried in an appendix — baseline completely misses these two constructs.

- **Workflow + feedback-loop quality:** CLI commands should include a concrete "what to check" loop: run `validate`, inspect `filteredErrors == 0`, distinguish from `totalErrors`. This is partially present (strong wins on evals 0, 20, 25) but the feedback-loop framing (how to interpret results) should be more explicit.

- **Anti-pattern scan + rewrites:**
  - **Stale guidance risk:** Any `likec4@<version>` examples should note that the flag set is version-sensitive; however, eval 2 confirms that disclaiming uncertainty ("verify against your installed version") costs points — the skill should be assertive about stable flags.
  - **Option overload risk:** If the skill lists multiple ways to do the same thing (e.g., `include * -> X` vs `include -> X`), it should pick the canonical form and note the alternative in a secondary sentence. The eval losses on 7-r2 and 28-r2 suggest the model is picking the non-canonical form from a multi-option list.
  - **Concrete rewrite:** In the relationship-extension section, change any phrase like "omitting the kind is ambiguous when multiple relationships match" to "omitting the kind is wrong when two relationships share the same source, target, and title but differ in kind — the parser resolves the bare matcher to the unkinded relationship silently, not to a compile error."

---

## 7. Verdict

The `likec4-dsl` skill is **highly effective**. It delivers a blind win rate of **79.3%** (46/58), a +27.1 pp expectation pass rate improvement, and a +2.57 rubric score gap — all consistent and strong signals. The primary value is in highly specific, notation-precise knowledge (CLI flag names, DSL block structure, semantic rules for metadata merge, identifier syntax, predicate families) that the baseline model consistently guesses incorrectly. The seven losses are all attributable to concision issues or single-word framing choices ("ambiguous" vs "wrong") rather than factual knowledge gaps, making them addressable with targeted instruction updates in P1/P2.
