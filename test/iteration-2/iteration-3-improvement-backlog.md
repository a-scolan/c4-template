# Iteration 3 Improvement Backlog

## Goal

Turn the iteration-2 findings into a focused improvement plan for skills, evals, and benchmark reliability.

## Implementation status

Repository changes corresponding to backlog items **B01–B08** have been applied on the current branch.

What remains after this implementation pass is the next full benchmark rerun and the measurement of the updated results.

## Companion backlog

This backlog is complemented by `iteration-3-agent-hook-backlog.md`, which tracks the custom benchmark agents and agent-scoped hook work needed to strengthen benchmark isolation, including the always-required blind comparator path.

## Prioritization

- **P0**: clear regression or negative quality delta; fix before any new broad benchmark run
- **P1**: skill/eval is useful but under-discriminating or under-performing; improve in the next pass
- **P2**: optimization work; improve cost, brevity, or reporting reliability after P0/P1

## Target outcomes for iteration 3

- Recover positive blind advantage on the most regressed skills
- Reduce non-informative ties on weak eval suites
- Keep strong skills strong while cutting unnecessary verbosity/time
- Eliminate incomplete benchmark metrics such as missing `files_read_count`

## Backlog summary

| ID | Priority | Work item | Main files | Expected outcome |
|---|---|---|---|---|
| B01 | P0 | Make `create-element` answer concrete first | `.github/skills/create-element/SKILL.md`, `.github/skills/create-element/evals/evals.json` | Recover wins by preferring direct snippets over pure routing |
| B02 | P0 | Make `create-relationship` more demonstrative | `.github/skills/create-relationship/SKILL.md`, `.github/skills/create-relationship/evals/evals.json` | Recover wins with stronger rule+example answers |
| B03 | P1 | Reframe `understand-project-structure` for onboarding and handoff clarity | `.github/skills/understand-project-structure/SKILL.md`, `.github/skills/understand-project-structure/evals/evals.json` | Better onboarding relevance and fewer losses on framing prompts |
| B04 | P1 | Improve `troubleshoot-errors` answer structure | `.github/skills/troubleshoot-errors/SKILL.md` | Turn stylistic losses into ties or wins |
| B05 | P1 | Harden weakly discriminating evals for config/sync/deployment | `configure-project-includes/evals/evals.json`, `sync-with-template/evals/evals.json`, `model-deployment-infrastructure/evals/evals.json` | Fewer ties, more meaningful blind outcomes |
| B06 | P1 | Add MCP-unavailable fallback behavior to core skills | `create-element`, `create-relationship`, `understand-project-structure`, `troubleshoot-errors`, `test-model` SKILLs | Better benchmark robustness when MCP tools are unavailable |
| B07 | P2 | Reduce cost/verbosity on strong but expensive skills | `design-view/SKILL.md`, `create-sequence-view/SKILL.md`, `implement-pattern/SKILL.md`, `test-model/SKILL.md` | Preserve quality with less time and/or shorter responses |
| B08 | P2 | Fix benchmark instrumentation gaps | `test/scripts/skill_suite_tools.py` and/or run-metrics production flow | No `null` values for key consumption metrics |

## Detailed work items

### B01 — `create-element` should answer with a concrete declaration first

**Why**
- Iteration 2 blind win rate: `0.0`
- Negative rubric delta
- Real examples show the skill often answers with process or handoff before giving a usable LikeC4 declaration

**Actions**
- Add an explicit response pattern in `SKILL.md`:
  1. recommend the element kind
  2. provide a minimal declaration
  3. mention the next skill only if needed
- Add a short section: **Direct answer first, handoff second**
- Add two canonical examples:
  - internal `Container_Api`
  - external `System_External`
- Add a rule: if the user asks what to model, do not answer with routing alone

**Eval updates**
- Strengthen prompts 2 and 3 so that a purely abstract answer loses against one that gives a concrete declaration
- Add at least one expectation that rewards an immediately usable snippet when the prompt asks for concrete modeling guidance

**Definition of done**
- Blind win rate > `0.5`
- Rubric delta > `0`

### B02 — `create-relationship` should teach by contrast, not only by rule

**Why**
- Iteration 2 blind win rate: `0.0`
- Negative rubric delta
- The skill usually passes expectations but loses on clarity, contrast, and example quality

**Actions**
- Add a fixed response structure in `SKILL.md`:
  1. relationship choice
  2. short rule
  3. minimal example
  4. counter-example
  5. handoff to `create-sequence-view` when timing matters
- Expand examples for:
  - `reads` vs `calls`
  - `writes` for persistence
  - cache + DB fallback with two `reads`
- Make the fallback-to-sequence guidance more explicit

**Eval updates**
- Tighten expectations to reward answers that both explain the rule and show a consistent example
- Add one expectation that a fallback scenario must mention explicit read relationships rather than only a verbal rule

**Definition of done**
- Rubric delta positive
- No blind loss caused purely by weaker examples

### B03 — `understand-project-structure` should optimize for onboarding and preflight framing

**Why**
- Large regression vs iteration 1
- Correct on taxonomy, but sometimes less relevant for “how do I enter this repo safely?” prompts

**Actions**
- Rework `SKILL.md` around two modes:
  - **preflight for editing**
  - **onboarding for new contributors**
- Clarify source-of-truth order:
  1. active project
  2. shared specs
  3. project config and model/view files
  4. skills as workflow guidance
- Add an explicit caution: example projects are useful references but not the primary semantic source of truth
- Add a short handoff template to `c4-modeling-process`

**Eval updates**
- Add expectations that distinguish:
  - `.github/skills/` as workflow guidance
  - `projects/shared/spec-*.c4` as semantic source of truth
- Add expectations that reward explicit active-project validation before referencing example projects

**Definition of done**
- Rubric delta > `0.3`
- Better wins on onboarding-style prompts

### B04 — `troubleshoot-errors` should answer in diagnosis format

**Why**
- Expectations pass on both sides, but the skill still loses quality comparisons
- The issue looks more like answer structure than factual correctness

**Actions**
- Add a mandatory response shape:
  1. probable error category
  2. root cause
  3. verification step
  4. minimal fix
- Add a compact “fix template” for common failures:
  - unknown kind
  - wrong FQN
  - deployment relationship in `model {}`
  - dynamic-view parent/child error
- Prefer one corrected snippet over long prose

**Definition of done**
- Convert current losses into ties or wins without making the skill longer

### B05 — Strengthen weakly discriminating eval suites

#### `configure-project-includes`

**Problem**
- Most comparisons are ties or near-ties
- Expectations are too easy for a solid baseline to satisfy

**Actions**
- Add cases that force explicit reasoning about:
  - append vs replace in `include.paths`
  - alias collision strategy
  - config-only change vs true multi-project reorganization
- Reward explicit resolution-order reasoning and concrete JSON edit proposals

#### `sync-with-template`

**Problem**
- Too many ties; prompt set often behaves like generic Git advice

**Actions**
- Add cases with mixed diffs that contain both syncable and local-only content
- Add one rollback scenario where a `sync/*` branch is already polluted by local files
- Reward explicit genericity/confidentiality decisions, not only command correctness

#### `model-deployment-infrastructure`

**Problem**
- The skill is often correct but not sufficiently differentiated

**Actions**
- Add prompts that force honest deployment modeling choices:
  - managed Kubernetes without invented VMs
  - `instanceOf` boundaries
  - inherited app traffic vs infra-only exceptions
- Reward answers that choose the right abstraction level, not just hierarchical boilerplate

### B06 — Add “If MCP is unavailable” fallback to benchmark-critical skills

**Why**
- The benchmark forbids MCP tools
- Some skills still rely too heavily on MCP-first phrasing, which weakens their offline usefulness

**Target skills**
- `create-element`
- `create-relationship`
- `understand-project-structure`
- `troubleshoot-errors`
- `test-model`

**Actions**
- Add a short fallback block for each skill:
  - answer from known repository conventions
  - provide a minimal example first
  - list verifications to run later once tooling is available

**Definition of done**
- Skills remain useful and specific in benchmark conditions without becoming anti-MCP in normal usage

### B07 — Optimize strong but expensive skills

#### `design-view`
- Move more long-form examples to `PATTERNS.md`
- Keep `SKILL.md` focused on selection rules and one short scaffold
- Default to concise answers unless the user explicitly asks for a full worked example

#### `create-sequence-view`
- Keep quality, but shorten default responses
- Prefer one good snippet + one anti-pattern instead of re-explaining the entire theory every time

#### `implement-pattern`
- Preserve quality, reduce detours and duplicated explanation
- Check whether common mini-patterns should become compact reusable scaffolds

#### `test-model`
- Introduce a “quick validation” mode vs “full validation” mode
- Avoid always expanding the full workflow when the prompt asks for a narrow sanity check

**Definition of done**
- Quality stays positive
- Time and/or verbosity reduced on next iteration

### B08 — Improve benchmark instrumentation reliability

**Why**
- Some summaries still contain missing `files_read_count`
- This weakens consumption analysis

**Actions**
- Trace why some `with_skill` runs record `null` for file reads
- Standardize run-metrics generation so all runs emit the same keys
- Add a post-run validation step that flags incomplete metrics before aggregation

**Definition of done**
- No `null` values for expected run metrics in the next iteration

## Suggested execution order

### Phase 1 — Fix the biggest quality regressions
1. B01 `create-element`
2. B02 `create-relationship`
3. B03 `understand-project-structure`
4. B04 `troubleshoot-errors`

### Phase 2 — Make the benchmark more discriminating
5. B05 `configure-project-includes`
6. B05 `sync-with-template`
7. B05 `model-deployment-infrastructure`
8. B03/B05 `understand-project-structure` eval hardening

### Phase 3 — Improve robustness and cost
9. B06 MCP-unavailable fallback blocks
10. B07 cost/verbosity optimization on strong skills
11. B08 instrumentation cleanup

## Exit criteria before iteration 3 benchmark

- All P0 changes applied and reviewed
- All updated eval files checked for discrimination quality
- No skill edited without a corresponding baseline-aware rationale from iteration 2
- Benchmark instrumentation produces complete metrics
- Iteration-3 scope is frozen before rerunning the full suite
