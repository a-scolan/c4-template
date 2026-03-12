No—this kind of help is not for repository tooling or CI/CD changes such as a GitHub Actions workflow update.

An ADR is best reserved for architectural decisions that materially affect the system design, major technology boundaries, or long-lived structural trade-offs. A repository workflow update is usually a tooling or delivery-process change, not an architecture decision.

Instead of forcing an ADR, a better fit would be one of these:
- a short note in the repository `README.md`
- a CI/CD or operations document
- a changelog or maintenance note in the repo
- an inline comment in the workflow if the change is small but important

If the workflow change reflects a broader architectural policy—for example a new release governance model or mandatory deployment gate—you could document that policy separately, then decide whether it deserves an ADR.