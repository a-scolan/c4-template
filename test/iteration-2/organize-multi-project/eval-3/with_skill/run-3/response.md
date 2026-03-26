Separate concerns, don’t centralize everything.

Recommended architecture for sharing:
- `projects/shared/` for technical conventions/specifications
- domain project folders for business models
- optional curated `domain-common` project for cross-domain reusable business assets

How to keep it from becoming a maze:
1. Keep shared technical specs stable and generic.
2. Promote business models to shared only when multiple projects demonstrably reuse them.
3. Assign clear ownership to any shared-domain artifact.
4. Avoid deep dependency chains between domain projects.

This preserves reuse while keeping navigation and maintenance straightforward.