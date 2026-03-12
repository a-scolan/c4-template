# Iteration 3 Agent Hook Backlog

## Goal

Introduce VS Code custom benchmark agents with agent-scoped hooks to enforce stronger **in vitro** isolation during skill benchmarks, while preserving the existing benchmark protocol where needed.

## Why this track exists

Iteration 2 showed that benchmark quality depends not only on better skills and evals, but also on tighter control over what benchmark workers are allowed to read during each phase.

This backlog adds a dedicated benchmark-isolation workstream for:

- baseline runs that must not read workspace skills
- `with_skill` runs that should ideally read only the target skill
- blind comparison runs that must remain blind to the real mapping

## Non-negotiable constraints

- **Blind comparison remains mandatory.** The blind comparator is not optional and must stay isolated from mapping and non-blind artifacts.
- **Physical skill relocation remains the baseline guarantee.** Agent-scoped hooks strengthen isolation, but do not replace the current `.github/skills/` relocation step for strict `without_skill` baselines.
- **Hooks are VS Code-specific and preview-only.** They require `chat.useCustomAgentHooks = true`.
- **Windows cannot rely on terminal sandboxing.** File-access control must be enforced via tool restrictions and `PreToolUse` hooks, not terminal sandbox settings.
- **GitHub-compatible structure, VS Code-scoped enforcement.** Agent files should remain valid `.agent.md` files with GitHub-documented frontmatter where possible, but hook enforcement is a VS Code-only extension.

## Intended outcomes

By the end of this track, the repository should support three benchmark-specific agents:

1. **Baseline benchmark agent**
   - read-only
   - cannot read `.github/skills/**`
   - cannot edit files or run terminal commands

2. **Targeted with-skill benchmark agent**
   - can read one allowed skill only
   - cannot read unrelated skills
   - can still read repo files needed to answer accurately

3. **Blind comparator agent**
   - can read `A.md`, `B.md`, and the target skill `evals.json`
   - cannot read `blind-map.json`
   - cannot read `with_skill/` or `without_skill/` raw outputs
   - cannot read `SKILL.md`

## Priority legend

- **P0**: required before relying on the new benchmark-agent workflow
- **P1**: important for maintainability, scaling, or repeatability
- **P2**: optimization or hardening after the core path works

## Backlog summary

| ID | Priority | Work item | Main files | Expected outcome |
|---|---|---|---|---|
| A01 | P0 | Scaffold workspace custom-agent structure | `.github/agents/`, `.github/agents/scripts/` | Stable home for benchmark agents and hook scripts |
| A02 | P0 | Create baseline benchmark agent | `.github/agents/skill-benchmark-baseline.agent.md` | Read-only benchmark agent with no skill-file access |
| A03 | P0 | Create shared access-policy hook engine | `.github/agents/scripts/enforce-test-access.py` | Deterministic path and tool filtering at `PreToolUse` |
| A04 | P0 | Create blind comparator agent | `.github/agents/skill-blind-comparator.agent.md` | Blind comparator with strict file allowlist |
| A05 | P0 | Define targeted `with_skill` agent strategy | `.github/agents/skill-benchmark-with-skill.agent.md` and/or generator script | Limit skill-enabled runs to one target skill |
| A06 | P1 | Add policy fixtures and dry-run tests for hook logic | `test/scripts/` and/or `.github/agents/scripts/tests/` | Safer iteration on hook rules without manual chat sessions |
| A07 | P1 | Integrate benchmark harness with custom agents | `test/scripts/skill_suite_tools.py`, benchmark orchestration notes | Repeatable use of the right agent per benchmark phase |
| A08 | P1 | Add setup and diagnostics documentation | `README.md`, benchmark backlog docs | Clear activation steps and troubleshooting guidance |
| A09 | P1 | Add blind-isolation validation checks | benchmark post-run validation flow | Detect comparator contamination early |
| A10 | P2 | Reassess whether hooks can safely reduce future relocation complexity | benchmark protocol docs | Document the boundary between hook isolation and physical isolation |

## Detailed work items

### A01 — Scaffold `.github/agents/` and shared scripts folder

**Why**
- The repository currently has skills, but no custom agent workspace.
- Benchmark agents should live in a stable, team-visible location.

**Planned files**
- `.github/agents/`
- `.github/agents/scripts/`

**Actions**
- Create the folder structure used by VS Code custom agents.
- Keep hook logic in scripts rather than inline shell one-liners.
- Prefer Python for policy evaluation because it is easier to test on Windows.

**Definition of done**
- Folder structure exists and is discoverable by VS Code.
- Script location is stable for all agent frontmatter references.

### A02 — Create `skill-benchmark-baseline.agent.md`

**Why**
- Baseline runs need a repeatable read-only agent persona.
- Tool restriction should reduce accidental contamination before the hook even runs.

**Recommended frontmatter direction**
- `target: vscode`
- `tools`: read/search only
- `agents: []` to block subagent use unless explicitly revisited
- `hooks.PreToolUse` calling the shared policy script
- optional `SessionStart` hook to inject audit context

**Baseline policy intent**
- allow reads under:
  - `projects/**`
  - `test/**`
  - selected root docs such as `README.md`
- deny reads under:
  - `.github/skills/**`
  - `.github/agents/**` (except the enforcement script if needed)
  - `.github/prompts/**`
  - `.github/instructions/**`
- deny edit and terminal tools entirely

**Important note**
This agent complements but does **not** replace the physical relocation of `.github/skills/` during `without_skill` runs.

**Definition of done**
- Baseline agent can answer benchmark prompts from repo context.
- Attempts to access skill files are denied by hook policy.
- The agent stays read-only.

### A03 — Create `enforce-test-access.py` as the shared hook engine

**Why**
- All benchmark-specific agents need deterministic policy enforcement.
- Reusing one engine avoids duplicating logic across multiple `.agent.md` files.

**Responsibilities**
- Read JSON hook payload from stdin.
- Inspect `tool_name` and `tool_input`.
- Apply policy based on environment variables or agent mode.
- Return JSON output with `permissionDecision: allow | deny | ask`.
- Emit clear reasons for denied access.

**Planned policy modes**
- `baseline`
- `with_skill_targeted`
- `blind_compare`

**Policy inputs**
- `BENCH_MODE`
- `BENCH_TARGET_SKILL` (for targeted with-skill runs)
- optional `BENCH_ITERATION`

**Definition of done**
- Hook denies out-of-scope file reads deterministically.
- Policy behavior is stable across Windows and Unix-like environments.
- Error messages are understandable enough for debugging hook decisions.

### A04 — Create `skill-blind-comparator.agent.md`

**Why**
- Blind comparison is mandatory and should become more rigorously isolated.
- Today, blindness is enforced procedurally. This agent should enforce it technically too.

**Allowed inputs**
- `test/iteration-N/<skill>/eval-*/blind/A.md`
- `test/iteration-N/<skill>/eval-*/blind/B.md`
- `.github/skills/<skill>/evals/evals.json`

**Denied inputs**
- `blind-map.json`
- `with_skill/response.md`
- `without_skill/response.md`
- `*-summary.json`
- `*-run-metrics.json`
- any `SKILL.md`

**Tool strategy**
- read/search only
- no edit tools unless the workflow explicitly needs the comparator to write its output file directly

**Open design choice**
- either let the blind comparator agent write `blind-comparisons.json`
- or keep it read-only and have the orchestrator write the file from the returned payload

**Recommended first step**
Start with direct file writing if the agent needs to stay self-contained, but keep the allowlist tight.

**Definition of done**
- Comparator can complete a blind comparison without access to mapping or non-blind artifacts.
- Hook policy blocks known contamination paths.

### A05 — Define the targeted `with_skill` strategy

**Why**
- The main remaining contamination risk in `with_skill` mode is accidental reading of unrelated skills.

**Recommended direction**
Support exactly one allowed skill per run.

**Two implementation options**

#### Option A — one generated agent per skill run
- Generate an agent file that bakes in the target skill path.
- Simpler policy logic.
- More files generated during runs.

#### Option B — one reusable agent + environment variables
- Reuse one `.agent.md` file.
- Pass the target skill through `BENCH_TARGET_SKILL`.
- More flexible, but requires reliable orchestration.

**Recommendation**
- **V1:** start with one reusable agent plus `BENCH_TARGET_SKILL`
- **Fallback:** switch to generated per-skill agents if hook input or orchestration proves brittle

**Allowed reads in this mode**
- `.github/skills/<target>/SKILL.md`
- `.github/skills/<target>/evals/evals.json`
- repository files needed to answer the prompt

**Denied reads**
- `.github/skills/<other-skill>/**`
- unrelated custom-agent files if not needed

**Definition of done**
- A `with_skill` run can read exactly one skill directory.
- Reading any other skill directory is denied.

### A06 — Add policy fixtures and dry-run tests for the hook script

**Why**
- Hook logic is security-sensitive and easy to regress.
- We need a fast way to validate policies without repeatedly driving VS Code chat manually.

**Actions**
- Add representative JSON fixtures for:
  - allowed read
  - denied read
  - denied skill access
  - blind comparator denied access to `blind-map.json`
- Add a small local runner to feed fixture JSON into the hook script and assert outputs.

**Definition of done**
- Policy logic can be tested offline.
- Regressions in allowlist/denylist behavior are caught before live runs.

### A07 — Integrate the benchmark harness with agent selection

**Why**
- The benchmark flow currently orchestrates runs procedurally.
- If custom agents become part of the standard process, the harness should document or help enforce which agent goes with which phase.

**Actions**
- Add benchmark notes or wrapper logic describing:
  - baseline phase → `skill-benchmark-baseline`
  - with-skill phase → `skill-benchmark-with-skill`
  - blind comparison → `skill-blind-comparator`
- Decide whether orchestration is manual, semi-automated, or fully generated.

**Definition of done**
- The intended agent per phase is explicit and repeatable.
- Future iterations do not depend on memory alone.

### A08 — Add setup and diagnostics documentation

**Why**
- Hooks are preview features and troubleshooting will matter.

**Documentation topics**
- enable `chat.useCustomAgentHooks`
- where the agent files live
- where the hook script lives
- how to inspect hook output in the VS Code output channel
- how to use `#debugEventsSnapshot` or Agent Debug logs to inspect actual tool payloads
- reminder that Windows terminal sandboxing is not the enforcement mechanism here

**Definition of done**
- A contributor can enable and debug the benchmark agents without reverse-engineering the setup.

### A09 — Add blind-isolation validation checks

**Why**
- Even with a blind comparator agent, we should verify the run did not accidentally read forbidden artifacts.

**Actions**
- Add a benchmark validation step that checks the comparator path assumptions.
- Optionally log denied attempts from the hook for auditability.
- Fail fast if blind-comparison artifacts are incomplete or suspicious.

**Definition of done**
- Blind comparison failures are easier to detect and diagnose.

### A10 — Reassess hook isolation versus physical isolation

**Why**
- Once the hook-backed agents are working, we should document what they can and cannot replace.

**Expected conclusion**
- Keep physical skill relocation for strict baseline isolation.
- Use hooks to reduce accidental reads and strengthen comparator discipline.
- Do not claim hook-only isolation is enough until proven with repeated benchmark runs.

## Suggested execution order

### Phase 1 — Core enforcement path
1. A01 scaffold agent folders
2. A03 build shared policy hook engine
3. A02 baseline benchmark agent
4. A04 blind comparator agent
5. A05 targeted with-skill strategy

### Phase 2 — Repeatability and safety
6. A06 policy fixtures and dry-run tests
7. A08 setup and diagnostics documentation
8. A07 harness integration notes
9. A09 blind-isolation validation checks

### Phase 3 — Reassessment and simplification
10. A10 document the boundary between hooks and physical isolation

## Acceptance criteria before adoption in the benchmark workflow

- The baseline benchmark agent cannot read `.github/skills/**`.
- The targeted with-skill agent cannot read unrelated skills.
- The blind comparator agent cannot read `blind-map.json` or raw non-blind outputs.
- Hook decisions are testable outside a live chat session.
- The setup is documented clearly enough for reuse in iteration 3.

## Risks and caveats

- **Preview feature risk:** agent-scoped hooks may change behavior in future VS Code updates.
- **Windows caveat:** terminal sandbox settings are not a solution for this repository’s main development environment.
- **Tool-schema drift:** actual tool names and input shapes must be confirmed in Agent Debug logs before hardening the final policy.
- **Partial isolation risk:** hooks control tool usage, not already-loaded context. Strict `without_skill` baselines still need physical skill relocation.

## Nice-to-have follow-up

If the core path works, consider a small generator that emits benchmark agent files or mode-specific frontmatter automatically for each skill and iteration.
