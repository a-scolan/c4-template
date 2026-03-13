1. probable error category: dynamic-view scope error plus invalid layout constraint.
2. root cause: `system -> system.api` models a parent calling its own child. In a dynamic view, that is a containment relationship, not a real interaction, so it breaks conceptually. `rank same user, system.api` is also invalid because `rank same` only applies to elements that are siblings under the same parent context; a root actor and a nested child are not siblings.
3. verification step: inspect the dynamic-view participants and their containment chain. If one endpoint contains the other, the interaction is modeled at the wrong level. Then verify whether the ranked elements truly share the same parent.
4. minimal fix: have the actor or an external peer call the child directly, and remove the invalid rank hint or replace it with one that only targets true siblings.

Example:
`user -> system.api 'Starts request'`
If you still need layout help, use a sibling rank only where valid, for example `rank same system.web, system.api` when both are children of `system`.
