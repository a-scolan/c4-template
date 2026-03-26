In most cases: **No, this does not warrant an ADR with `document-decision`.**

Reason: a GitHub Actions workflow update is usually repository/process tooling, while this skill is for long-lived architecture decisions and trade-offs.

## Use ADR only if architecture is truly affected
Potential ADR-worthy cases:
- deployment strategy change with system-level consequences
- compliance/security enforcement that changes architecture boundaries or runtime controls

If it is a normal CI workflow tweak, prefer:
- PR explanation
- changelog/engineering notes
- operations docs update when needed
