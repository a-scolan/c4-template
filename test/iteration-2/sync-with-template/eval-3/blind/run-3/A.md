## Repeatable long-term sync workflow

1. Keep local work committed before every sync cycle.
2. Create a dedicated `template-sync` branch.
3. Pull template updates into that branch.
4. Review shared specs and project config first.
5. Resolve path, include, alias, tag, relationship-kind, and element-kind drift.
6. Re-check project model files for references broken by shared changes.
7. Re-render and inspect key views.
8. Document any deliberate local divergence so the next sync is faster.
9. Merge only after the workspace parses and the diagrams still tell the right story.

For ongoing hygiene:
- sync on a regular cadence instead of after long gaps
- keep template-owned and project-owned responsibilities clear
- record local exceptions in ADRs or project notes
- avoid editing shared template files inside a project unless you truly want to own the fork

The workflow should be branch-based, compare-first, and validation-heavy. Boring is good here; boring keeps diagrams alive.