Yes—`where source.tag is #next` will match that relation.

`prod.eu.frontend` is a deployed instance (`instanceOf frontend`). For deployment instances, tags are **effective as a union**:
- tags on the logical element (`frontend` has `#next`), plus
- tags added on the deployed instance itself (`#gamma`).

So the source instance `prod.eu.frontend` is considered to have both `#next` and `#gamma`.

Therefore:
- `include prod.eu -> prod.db where source.tag is #next` → **matches** (via inherited tag from `frontend`)
- `where source.tag is #gamma` → **also matches** (tag defined directly on the instance)

In short: deployment instances inherit tags from their `instanceOf` element, and instance-level tags are additive.