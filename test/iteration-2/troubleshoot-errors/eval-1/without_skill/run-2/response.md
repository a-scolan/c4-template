The break is caused by syntax/context mismatch in the dynamic view, not by `rank` alone.

What is happening:
- `system -> system.api` often indicates mixed identifiers (parent and child FQN) where the view expects valid resolvable participants in that scope.
- Then `rank same user, system.api` fails because layout directives only work with valid nodes already present/resolved in the view.

Real cause:
- At least one referenced node id is invalid for that dynamic view scope (or unresolved), so the later rank directive also fails.

What to fix:
- Use correct, declared ids/FQNs consistently for dynamic steps.
- Ensure both `user` and `system.api` are valid participants in that view context before ranking.
- If needed, normalize to one naming style and confirm declarations first, then apply `rank same`.