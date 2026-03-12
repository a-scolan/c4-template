That is usually **not** a good idea.

`projects/shared/` should contain only reusable definitions such as shared specs, tags, styles, relationship kinds, and assets. It should **not** hold project-specific business models.

So if `paymentsCore` and `backOfficeUser` belong to the payments domain, keep them in the owning project, for example in `projects/payments/system-model.c4`.

For cross-project references, keep them explicit, minimal, and non-circular:

- If something is truly shared and external to several projects, define a small shared external abstraction that all projects can reference.
- If shared business concepts deserve their own ownership boundary, create a dedicated project such as `projects/externals/` or another clearly named domain project.
- Do **not** make projects include each other in a loop.

A good rule is:

- `projects/shared/` = reusable conventions and assets
- owning project = domain actors/systems/containers
- cross-project references = documented, minimal, one-way where possible
