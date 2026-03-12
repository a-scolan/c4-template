Probably not for a plain GitHub Actions workflow change.

Repository tooling / CI-CD updates are usually operational or maintenance changes, not architecture decisions. An ADR is a better fit when the change affects the system’s runtime structure, major technology direction, security boundaries, ownership boundaries, or long-lived architectural constraints.

So for a normal workflow edit, avoid forcing an ADR.

Better alternatives:
- update the repository `README.md` if contributors need to understand the new workflow behavior
- add a short note in an ops or engineering docs page
- document the reason directly in the workflow file or in a repo-level change log
- open a lightweight repo note or engineering decision log entry if the team wants traceability

Write an ADR only if the workflow change represents a broader architectural governance decision, such as a new release-control model, a mandated security gate, or a delivery design that materially changes how the platform is operated.
