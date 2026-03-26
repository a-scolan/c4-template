It’s generally a **bad practice** to place `paymentsCore` and `backOfficeUser` in the shared specifications area.

Why:
- Shared specs are for reusable taxonomy/conventions (kinds, tags, styles, relationship definitions).
- `paymentsCore` and `backOfficeUser` are domain model instances and should live in a domain project (for example `projects/payments`).

How to handle cross-project references correctly:
1. Keep cross-project links explicit and limited.
2. For third-party/common externals, define them once in a shared external model (or dedicated `externals` project).
3. Let each project reference those externals via normal relationships.
4. Prevent circular include graphs; `shared` should be dependency source, not consumer.

So: yes to shared conventions, no to dumping domain entities into shared specs.