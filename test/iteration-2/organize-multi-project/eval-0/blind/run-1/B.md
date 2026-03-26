To bootstrap a new **payments** project cleanly in a multi-project LikeC4 workspace, use a minimal baseline and wire shared specs explicitly.

1. Create a new folder: `projects/payments/`
2. Add exactly these minimum files:
   - `projects/payments/likec4.config.json`
   - `projects/payments/system-model.c4`
   - `projects/payments/system-views.c4`
3. In `likec4.config.json`, set a unique project name/title and include shared specs using a **relative path** (for example `../shared`).
4. Keep image aliases consistent with other projects (especially the shared images alias).
5. Start the model with only the payments domain elements you need now (no copy/paste of example systems).
6. Add views that match current needs (typically one context/container view first); expand later to deployment/dynamic views only when required.

A practical starter config shape is:
- unique `name`
- descriptive `title`
- `include.paths` referencing `../shared`
- consistent `imageAlias` entries used across the workspace

Key guardrails:
- Do **not** place payments-specific systems in `projects/shared/`
- Do **not** use absolute include paths
- Do **not** clone an example project verbatim; treat it as scaffold only

This gives you a clean, maintainable project boundary with shared conventions reused correctly.