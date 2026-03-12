The breakage comes from two different conceptual problems.

1. `mySystem -> mySystem.api` is not a valid dynamic interaction.
	A parent should not call its own child in a dynamic view, because that is structural containment, not a runtime interaction between peers. The fix is to show the real caller directly, such as `user -> mySystem.api`, or `user -> mySystem.webapp` and then `mySystem.webapp -> mySystem.api` if the web application is the actual intermediary.

2. `rank same user, mySystem.api` is a layout error.
	`rank same` only works for elements that share the same parent context. `user` is outside `mySystem`, while `mySystem.api` is inside it, so they cannot be ranked together as siblings.

Targeted fix:
- remove the parent-to-child interaction from the dynamic view
- model the real interaction path instead
- remove the cross-context `rank same`, or apply `rank same` only to true siblings such as `mySystem.webapp` and `mySystem.api`

So the real cause is not “dynamic views are flaky”; it is a parent-child interaction plus a cross-context rank constraint.
