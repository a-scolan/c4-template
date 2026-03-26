Not recommended.

`paymentsCore` and `backOfficeUser` are concrete business/domain model entities, so they should belong to the relevant domain project (for example `projects/payments`), not to the shared specifications area.

Use `projects/shared` for reusable specification artifacts only:
- kind definitions
- relationship taxonomy
- tags/styles/conventions

Cross-project reference pattern:
1. Keep references explicit and intentional.
2. Define truly common external systems once (shared external model or dedicated externals project).
3. Reference those systems from domain projects.
4. Keep dependency direction simple to avoid circular project coupling.

Bottom line: shared standards yes, shared domain instances no.