Add the `payments` project by creating a small, clean baseline first, then evolve.

Minimum bootstrap set:
- `projects/payments/likec4.config.json`
- `projects/payments/system-model.c4`
- `projects/payments/system-views.c4`

Bootstrap checklist:
1. Use a unique project `name` and clear `title` in config.
2. Point `include.paths` to shared specs with a relative path (typically `../shared`).
3. Reuse the same image aliases as other projects (including shared images alias) for consistency.
4. Add only payments-specific model elements initially.
5. Keep views minimal at start; add additional files only when complexity justifies it.

What to avoid:
- storing project-specific systems/actors in `shared`
- absolute include paths
- copying an example project unchanged

This keeps project boundaries clean and prevents long-term workspace drift.