# Copilot Workspace Instructions

Follow these steps for any change in this workspace:

1) Read .github/LLM-INSTRUCTIONS.md first.
2) MCP: LikeC4 (`list-projects`, `read-project-summary`, `search-element`, `find-relationships`, `open-view`); Context7 (resolve LikeC4 docs, max 3 syntax queries/task).
3) Validate: PascalCase kinds, camelCase vars; typed relationships + labels; tags → technology → description; FQN; deployment `instanceOf`; scoped includes, rank hints, no returns.
4) Tag scope: model tags from spec-global/context/containers/components; deployment tags from spec-deployment only; never repeat tags already in the element kind.
5) Sources: .github/LLM-INSTRUCTIONS.md; projects/shared/spec-*.c4. Re-check before saving.
6) ADR: Document system architecture decisions in `ADR/NNNN-decision-title.md` using standard ADR format (see ADR/0000-template.md); manually increment numbering; focus on design rationale for systems/containers/components in LikeC4 diagrams (e.g., why Kong vs HAProxy, why MongoDB vs PostgreSQL), not repo/tooling decisions.