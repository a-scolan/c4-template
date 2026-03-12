No—this skill is not the right fit for a GitHub Actions workflow change on its own.

This ADR skill is for architecture decisions in the system design, such as technology selection, architecture patterns, or deployment infrastructure choices. It is explicitly not for repository tooling or CI/CD changes.

Do not force an ADR here unless the workflow change reflects a broader architecture decision that materially affects the system itself.

Better alternatives for a normal workflow change:
- update `README.md` or contributor documentation;
- add a short note in an operations or engineering runbook;
- capture the rationale in the pull request description or a repo maintenance note.