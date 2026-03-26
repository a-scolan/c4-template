Follow this strict order without skipping:
1) Re-sync workspace context after shared-spec changes (kinds, tags, metadata, conventions).
2) Validate impacted model elements/relationships before adding new views.
3) Add the sensitive C3 view (only for the target container), applying proper scope and visibility controls.
4) Verify C3 consistency with C2/C1 and shared definitions.
5) Create the nominal user scenario as a dynamic view (time-ordered interactions).
6) Run final consistency and quality checks across projects.

Skills handoff order:
- understand-project-structure (first, because shared specs changed)
- sync-with-template or equivalent sync-oriented capability (if template/shared alignment is required)
- customize-view / design-view (for the sensitive C3 presentation rules)
- create-sequence-view (for nominal scenario dynamics)
- test-model (final validation)

Rationale: stabilize shared foundations first, then static structure (C3), then temporal behavior (dynamic), then validation.