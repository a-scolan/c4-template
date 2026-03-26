# Response — eval-1, without_skill, run 2

## Prompt

I just changed the repository's GitHub Actions workflow. Should I write an ADR with this skill?

## Response

Whether to write an ADR for a GitHub Actions change depends on whether the change constitutes an **architectural decision** — that is, a deliberate, consequential choice with notable trade-offs that you want to preserve reasoning for.

**Simple changes that do NOT need an ADR:**
- Version bumps for actions (`actions/checkout@v3` → `v4`)
- Adding a new step to an existing workflow
- Adjusting timeout or concurrency settings
- Fixing a broken path or environment variable

These are operational maintenance tasks. A PR description plus a commit message is sufficient documentation.

**Changes that may warrant an ADR:**
- Deciding to use GitHub Actions over an alternative CI system (Jenkins, GitLab CI, ArgoCD)
- Introducing a new build strategy with broad impact (e.g., matrix builds, monorepo build isolation)
- Adopting a new deployment pipeline model (e.g., GitOps with Flux, trunk-based deployment gates)
- Choosing a release strategy tool (Semantic Release, Changesets) that affects the entire team

**Practical test:**

Ask yourself: *"Would a new team member need context on why this was done this way rather than another way?"* If yes, write the ADR. If it's self-evident or trivial, skip it.

Based on what you described ("just changed the workflow"), it sounds like a maintenance update. Unless that change involved choosing between competing approaches with significant long-term impact, I would **not** write an ADR for it. A clear commit message is sufficient.
