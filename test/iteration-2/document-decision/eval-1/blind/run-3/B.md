# Response — eval-1, without_skill, run 3

## Prompt

I just changed the repository's GitHub Actions workflow. Should I write an ADR with this skill?

## Response

Generally, **no** — a routine GitHub Actions workflow change does not require an Architecture Decision Record.

ADRs are intended to capture **architectural decisions**: choices that significantly shape the structure, behavior, or constraints of the system, and where the reasoning behind the choice should be preserved for future reference.

A GitHub Actions workflow change is a **CI/CD process change**, not an architectural decision, unless:
- It represents a strategic platform choice (e.g., adopting GitHub Actions as the team's standard CI platform for the first time)
- It introduces a fundamentally new deployment or release practice affecting all developers
- It installs tooling that becomes a long-term architectural dependency

For day-to-day workflow edits — adjusting triggers, updating step versions, adding a linting check, fixing environment variables — a descriptive commit message and PR comment are sufficient documentation.

**When in doubt, ask:**
- Did we weigh this against a meaningful alternative?
- Will a team member 6 months from now reasonably wonder *why* this was done this way?
- Does this change constrain future architectural choices?

If the answer to most of these is no, skip the ADR and keep the commit history clean.
