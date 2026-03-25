`backend.api` is unresolved in `ops.c4` because that path is **not a valid global identifier** across files.

In LikeC4, nested names such as `backend.api` are relative to a parent scope. Here, `api` is defined under:

- `cloud` (system)
- `cloud.backend` (container)
- `cloud.backend.api` (service)

So from another file, `backend.api` has no top-level `backend` to resolve from. Cross-file references must use the element’s fully qualified name (FQN), rooted at the top element.

Use the relationship as:

`cloud.backend.api -> cloud.db`

(assuming `db` is also a child of `cloud`; if not, use its actual full FQN).