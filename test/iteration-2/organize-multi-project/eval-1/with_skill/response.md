No — that is **not** a good use of the shared specifications area.

`projects/shared/` should contain only **reusable definitions** such as shared kinds, tags, styles, and assets. A concrete `paymentsCore` system and a concrete `backOfficeUser` actor are **project-specific models**, so they should live in the owning project, for example `projects/payments/`.

For cross-project references, keep them **explicit, minimal, and non-circular**:
- If something is truly shared as an external dependency, define it once as a shared external system.
- If you have a broader set of shared external/business references, place them in a small dedicated project such as `projects/externals/`.
- Let multiple projects reference that shared external surface, but do **not** make project A depend on project B and project B depend on project A.

So the rule is simple:
- reusable specs/assets -> `projects/shared/`
- owned systems/actors like `paymentsCore` and `backOfficeUser` -> owning project
- truly shared externals -> shared external definition or dedicated `externals` project

That keeps the workspace clear and avoids circular dependencies.