Structured diagnosis for unknown kind/relationship:

## 1) Identify the failing namespace

- If failure is on elements, validate element kinds in shared specs.
- If failure is on deployment links, validate deployment relationship kinds.
- Do not mix model relationships (`calls`, `async`, `reads`, `writes`) with deployment protocol relationships (`https`, `tcp`, `sql`, etc.).

## 2) Check source of truth in this order

1. Active project confirmation
2. Project summary (explicit project)
3. Shared taxonomy:
   - `projects/shared/SPEC_CHEATSHEET.md`
   - `projects/shared/spec-context.c4`
   - `projects/shared/spec-containers.c4`
   - `projects/shared/spec-components.c4`
   - `projects/shared/spec-deployment.c4`
4. Project include wiring (`likec4.config.json`)

## 3) Compare expected vs actual

- Compare exact spelling/case of kind or relationship.
- Compare intended level (C1/C2/C3/deployment).
- Compare parent hierarchy and FQN.

## 4) Confirm before fixing

- Re-run project checks after any project switch.
- Validate target element exists in the same project.
- Apply minimal correction only after taxonomy match is proven.

This approach fixes root cause (context/taxonomy mismatch) instead of patching symptoms.