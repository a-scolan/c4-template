Not a good idea.

`projects/shared/` should contain **reusable specifications, conventions, and assets**, not project-specific business models.

So:

- keep `paymentsCore` in the owning payments project
- keep `backOfficeUser` in the owning project too, unless it is truly a shared actor used the same way across multiple projects

If something is genuinely shared across projects, model it explicitly as one of these:

1. a **shared external** that multiple projects can reference, or
2. a very small dedicated project for shared domain/external models

For cross-project references, keep them:

- **explicit**
- **minimal**
- **one-way**

A good rule is:

- projects can depend on `shared` specs
- projects may reference a clearly shared external/domain model
- projects should **not** depend on each other in a circular way

So do **not** move `paymentsCore` and `backOfficeUser` into the shared specs area just to make them visible everywhere. Put them where they are owned, and expose only truly shared concepts through a deliberate shared external/domain boundary.
