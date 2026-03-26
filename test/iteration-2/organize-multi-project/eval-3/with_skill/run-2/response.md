Separate them, but keep the structure simple.

A practical split:
- `projects/shared/` → technical conventions only (specs, styles, tags, reusable kinds)
- `projects/<domain>/` → business/domain models and domain views
- optional `projects/domain-common/` → truly reusable business concepts shared by multiple domains

This gives clarity without creating a maze:
- one clear shared technical layer
- optional curated shared business layer
- explicit domain ownership

Decision rule:
- If it is a convention or taxonomy: put it in shared specs.
- If it is domain behavior/model instance: keep it in a domain project.
- If multiple domains reuse it and ownership is clear: promote to a dedicated shared-domain project (not to low-level spec files).

That balance keeps the repo navigable and reusable.