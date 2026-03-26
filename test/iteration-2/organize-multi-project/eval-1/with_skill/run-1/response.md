Short answer: **not a good idea**.

`paymentsCore` (domain system) and `backOfficeUser` (domain actor) are project/business-model content, not reusable specification primitives. The shared area should contain reusable definitions (kinds, tags, styles, relationship taxonomy, global conventions), not project-owned model instances.

Recommended split:
- `projects/shared/`: reusable specs only
- `projects/payments/`: `paymentsCore`, payments actors, payments relationships
- optionally `projects/externals/`: external systems commonly referenced by multiple projects

For cross-project references, keep them explicit and minimal:
1. Put common external systems in a shared external model (or dedicated externals project).
2. Reference those externals from each project through normal relationships.
3. Document the dependency boundary so ownership is clear.
4. Avoid circular includes between projects; shared content should flow one-way from `shared` (or `externals`) into domain projects.

So: shared conventions everywhere, domain models in domain projects.