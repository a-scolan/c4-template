Split it progressively rather than doing a big-bang rewrite.

A practical baseline is:

- `likec4.config.json`
- `system-model.c4`
- `system-views.c4`

Recommended sequence:

1. Move all element and relationship definitions into `system-model.c4`.
2. Move the C1, C2, and C3 views into `system-views.c4`.
3. When use-case flows become numerous or noisy, extract them into a dedicated file such as `system-sequences.c4` instead of mixing them into every model/view file.
4. If deployment becomes a real concern, separate it into dedicated deployment files such as `deployment-model.c4` and `deployment-views.c4` (or a single `deployment.c4` first, then split later).
5. If operational topology or runbook-style views matter, separate those into dedicated operations files such as `operations-model.c4` and `operations-views.c4` (or `operations.c4` as a first step).

That gives you a clean baseline quickly: structural model in one file, C1/C2/C3 views in one file, then use cases, deployment, and operations extracted only when the model size justifies it.