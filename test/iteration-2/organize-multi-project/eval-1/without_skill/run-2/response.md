Usually not a good idea.

`paymentsCore` and `backOfficeUser` sound like concrete business elements, not shared specification primitives. In this workspace, `projects/shared/` is already acting as the reusable specification layer: common tags, relationship types, colors, and reusable context/container/component kinds. That is the right place for modeling conventions, not for every business actor or business system.

A better split is:
- put generic modeling building blocks in shared specs
- keep concrete project business elements local to the project that owns them
- move a concrete element into a shared business-model file only if it is intentionally reused by several projects and has stable semantics across them

For cross-project references, handle them explicitly instead of hiding them inside the shared spec layer:
- either model the external dependency locally in each project view/model where it matters
- or create a separate reusable shared domain file for truly common business elements, then import that file intentionally from the projects that need it

So: do not put `paymentsCore` and `backOfficeUser` into the shared specifications area just to make them visible everywhere. Visibility is not the same as reuse. Only promote them to shared business-model assets if multiple projects genuinely depend on the same canonical definition.