Not a good idea if `paymentsCore` and `backOfficeUser` belong to the payments domain.

Use `projects/shared/` only for reusable definitions that are intentionally generic and stable across projects: specs, tags, relationship kinds, common icons, and maybe a truly shared external system model.

Recommended ownership:
- Keep `paymentsCore` and `backOfficeUser` in `projects/payments/` if payments owns them.
- If something is genuinely shared across many projects, model it as a neutral shared external or place it in a dedicated `projects/externals/` project.

For cross-project references:
- Make them explicit and minimal.
- Give each business system one owning project.
- Let other projects reference only the few external elements they actually interact with.
- Avoid project A importing project B while project B also imports project A.

A simple rule that scales:
- `projects/shared/` -> reusable specs and assets only
- owning project -> project-specific business model
- optional neutral external/domain project -> truly shared business concepts

That keeps references clear and avoids circular dependencies.
