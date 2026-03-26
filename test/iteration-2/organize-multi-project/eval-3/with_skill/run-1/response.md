Don’t put everything into one shared bucket. Separate by intent:

- **Shared specs area** (`projects/shared/`): technical conventions only
  - element/relationship kinds
  - tags, styles, global defaults
  - reusable visual and taxonomy rules

- **Domain projects** (`projects/<domain>/`): business models
  - systems, actors, containers/components
  - domain relationships and views

If you have reusable business concepts used by many domains, create a focused shared-domain project (for example `projects/domain-common/`) instead of mixing them into low-level specs. Keep it small and curated.

A scalable pattern is:
1. Shared technical spec layer
2. Optional shared business-common layer (strictly reusable, owner defined)
3. Domain projects consuming those layers

This avoids both extremes:
- giant shared monolith
- over-fragmented maze of tiny projects

Rule of thumb: share conventions broadly, share business models selectively, keep ownership explicit.