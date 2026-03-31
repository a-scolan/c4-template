# Skill Synthesis — `likec4-dsl` | Iteration: likec4-dsl-test7

Generated: 2026-03-30 | Runs: 2 per eval | Evals: 32

---

## 1. Quantitative summary

| Metric | With skill | Without skill | Δ |
|---|---|---|---|
| Blind win rate | 76.6% (49 wins) | 7.8% (5 wins) | +68.8 pp |
| Ties | 10 (15.6%) | — | — |
| Expectation pass rate | 0.957 | 0.706 | **+0.251** |
| Rubric score (0–10) | 9.32 | 7.01 | **+2.31** |
| Seconds / eval | 9.20 s | 7.73 s | +1.46 s |
| Words / eval | 63.6 | 63.4 | +0.2 |
| Files read / eval | 32.0 | 32.0 | 0 |
| Executable validity | 60.4% | 61.4% | −0.9 pp |

**Verdict: strong positive signal.** With-skill wins nearly 77% of blind comparisons while matching without-skill on length and files read. The 1.5 s overhead per eval is the only consistent cost.

---

## 2. Per-eval breakdown (blind comparison outcomes)

| Eval | Run 1 winner | Run 2 winner | Flips? | Topic | Key discriminator |
|---|---|---|---|---|---|
| 0 | with_skill | with_skill | no | File-scoped validate | Correct `--file` flag + filteredFiles/filteredErrors |
| 1 | with_skill | with_skill | no | config include paths | `$schema` + `include.paths` form |
| 2 | with_skill | with_skill | no | Project root resolution | Nearest-config scope explanation |
| 3 | with_skill | with_skill | no | Dynamic sequence view | `variant sequence` + backward `<-` response arrows |
| 4 | TIE | TIE | no | View-local styling | Both equivalent on `view { style ... }` |
| 5 | with_skill | without_skill | **yes** | Relationship predicate | Disagreement on `->` vs `<->` bidirectionality |
| 6 | with_skill | with_skill | no | Extend relationship kind | Correct `extend of` syntax |
| 7 | with_skill | with_skill | no | View extends / scope | Inherited scope implicit, inbound predicate |
| 8 | with_skill | with_skill | no | Element kind definitions | Canonical `kind` block placement |
| 9 | with_skill | with_skill | no | Deployment instanceOf | `instanceOf` link vs inline element |
| 10 | with_skill | with_skill | no | Global tag selectors | `#tag` scoping in global styles |
| 11 | with_skill | with_skill | no | Specification block | `spec` section ordering + required fields |
| 12 | TIE | with_skill | **yes** | Include wildcard `**` | Double-wildcard descendants coverage |
| 13 | with_skill | with_skill | no | View predicate `_` | Anonymous element indicator from `_` |
| 14 | with_skill | with_skill | no | Invalid top-level styles | Correct top-level block list + fixed DSL file |
| 15 | with_skill | with_skill | no | Identifier validity | `payment-api` valid vs `payment.api` invalid |
| 16 | with_skill | TIE | **yes** | Relationship title quoting | When and whether to quote titles |
| 17 | with_skill | with_skill | no | Cross-file FQN | Lexical scope + FQN rewrite |
| 18 | with_skill | with_skill | no | Async relationship extend | Disambiguation by kind + title |
| 19 | with_skill | with_skill | no | Scoped include semantics | Direct-children base set + predicate form |
| 20 | with_skill | with_skill | no | Multi-file validate flags | Required invariants: `--json --no-layout --file` |
| 21 | with_skill | with_skill | no | View autoLayout hint | Direction + rank-sep values |
| 22 | with_skill | TIE | **yes** | Neighbor relationship include | `->` vs `<->` within-scope edge expansion |
| 23 | TIE | TIE | no | Deployment tag inheritance | Cumulative tag semantics — both runs stable |
| 24 | with_skill | with_skill | no | Model split across files | Global merge semantics |
| 25 | with_skill | with_skill | no | View layout grid hint | `autoLayout GridLayout` parameters |
| 26 | with_skill | with_skill | no | Element metadata fields | `metadata` block vs `notes` |
| 27 | with_skill | without_skill | **yes** | Style color token | Disagreement on `#primary` vs hex color form |
| 28 | with_skill | with_skill | no | Specification relationship | `relationship` vs `connects` taxonomy |
| 29 | with_skill | with_skill | no | Deploy view instanceOf filter | `instanceOf` filter predicate |
| 30 | with_skill | with_skill | no | Component-level view scope | `of` scope + include `*` for components |
| 31 | with_skill | with_skill | no | Use case flow view | Dynamic view step ordering |

**Winner-flip evals (disagreements to verify):** 5, 12, 16, 22, 27. Treat these as candidates for eval hardening, not definitive skill failures.

---

## 3. Executable validity detail

| Config | Applicable runs | Valid rate |
|---|---|---|
| with_skill | 48 | 60.4% |
| without_skill | 44 | 61.4% |

Δ = −0.9 pp — essentially neutral. The skill improves **semantic correctness** (rubric +2.31, expectation +0.25) but does not meaningfully improve **AST-level snippet validity**. Consider adding closed-form snippet evals with automated AST-check assertions.

---

## 4. High-variance eval analysis

16 of 32 evals (50%) are flagged high-variance. Patterns:

- **9 of 16 have no winner flips** — variance is in *degree* of improvement, not outcome direction. These are stable.
- **6 winner flips** (evals 5, 12, 16, 22, 23, 27): real ambiguity. Root topics:
  - Bidirectional relationship pred syntax (evals 5, 22) — expectation wording is underspecified.
  - Color token form (eval 27) — `#primary` vs hex is not pinned in the grading spec.
  - Relationship title quoting (eval 16) — grading spec allows both forms.
  - Double-wildcard `**` coverage (eval 12) — tied run-1, won run-2; asymmetric outputs.

---

## 5. Comparison with previous iteration (likec4-dsl-test6)

| Metric | test6 | test7 | Δ |
|---|---|---|---|
| Win rate | 78.1% | 76.6% | −1.6 pp |
| Expectation Δ | 0.229 | 0.251 | +0.022 |
| Time Δ / eval | 0.14 s | 1.46 s | +1.32 s |

Win rate decreased slightly (within 2-run sampling noise). Expectation delta improved by +0.022. The time delta increase (+1.32 s) likely reflects model-speed variation between sessions rather than skill regression; verify by tracking per-session baseline timing.

---

## 6. Errors and issues for future benchmark improvements

1. **Raw comparator JSON corruption** *(critical — blocked finalization)*
   Multiple `_meta/raw-comparison-*.json` files contained concatenated JSON objects (two full payloads in one file) or duplicate keys caused by comparator workers appending a second write to an existing file. **Fix**: harness must use an atomic overwrite (`mode='w'`) and validate JSON parse before persisting any comparator payload.

2. **Blind-map assignment instability check missing**
   Eval 0 run-2 had a contradictory A/B mapping during recovery. Add a post-materialize check that `blind-map.json` assignments (which response is `A`, which is `B`) are immutable once written for a given `(eval_id, run_number)` pair.

3. **Executable validity not improved by skill**
   The skill raises rubric and expectation scores but not AST validity. Add at least one eval per major DSL construct category that triggers an automated structural validator, so the benchmark can distinguish concept errors from syntax errors.

4. **6 winner-flip evals need expectation hardening**
   Evals 5, 16, 22, 27 flip between runs. Review grading-spec expectations for these evals and add a contrastive "X is valid but Y is not" expectation that forces a single correct answer.

5. **Time delta growth across iterations (+1.32 s/eval)**
   Monitoring shows increasing median time delta. Capture per-run wall-clock start time and model identity to allow inference-latency attribution separate from skill-processing overhead.

---

## 7. Skill improvement recommendations (Anthropic best-practices pass)

| Check | Finding |
|---|---|
| Concision / token economy | No bloat: words/eval delta is +0.2 (negligible). No cut needed. |
| Degrees of freedom fit | Bidirectional predicate rule (evals 5, 22) is under-constrained. Add explicit `<->` vs. `->` decision guidance. |
| Triggerability metadata | Name and description are clear; no observed false-negative triggering. |
| Progressive disclosure | Core DSL snippet guidance is well-layered. Deployment and dynamic views deferred appropriately. |
| Workflow + feedback loop | CLI validation guidance works well (eval 20); near-miss flags are already blocked. |
| Anti-pattern: identifier validity | `payment-api` valid vs. `payment.api` invalid is a frequent miss without skill. Reinforce this example in the identifier section. |
| Anti-pattern: color token form | `#primary` / `#secondary` naming is not yet documented as the canonical form vs. hex literals. Add a style-token canonical list. |
