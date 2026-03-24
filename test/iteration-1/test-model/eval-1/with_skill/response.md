Use a quick validation focused on view scope and context:
1. Check parent context first: a C2 view must show the parent system boundary around the web application and API, plus the external neighbor such as `user`. If the containers render without the containing system, the view is incomplete even if the syntax is valid.
2. Check include scope: prefer explicit FQNs or a pattern scoped to the parent system. Avoid `include **`; that is the classic over-broad include.
3. Preview the view and look for symptoms of a broad include: unrelated sibling containers, extra external actors, or elements from outside the intended system.
4. Tighten the include until only the system boundary, the web app, the API, and the relevant actor remain.
5. Recheck that the web app and API FQNs still resolve after any include change.

Rule of thumb: for C2, keep the parent system visible and make the include as narrow as possible.
