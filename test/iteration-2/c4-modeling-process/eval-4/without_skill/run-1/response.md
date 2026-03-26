It should **not** detail everything itself.

`c4-modeling-process` should act as the orchestration flow:

1. confirm C2 is stable,
2. decide what detail is needed next,
3. hand off to specialized skills.

For your two goals:

- **Production infrastructure** -> rely on `model-deployment-infrastructure` (and, if needed, `structure-deployment-tiers` / `name-deployment-nodes`).
- **Nominal user scenario** -> rely on `create-sequence-view`.

So: this skill defines order and gating decisions; specialized skills provide deep implementation detail.