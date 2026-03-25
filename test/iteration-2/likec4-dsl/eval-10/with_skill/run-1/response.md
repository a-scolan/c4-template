**`where source.tag is #next`** → **Yes, it matches** `prod.eu.frontend`. A deployed instance inherits all tags from its logical model element. Because `frontend` carries `#next` in the logical model, and `prod.eu.frontend` is `instanceOf frontend`, `#next` is present in the effective tag set of the deployed instance. The predicate therefore evaluates to true.

**`where source.tag is #gamma`** → **Yes, it also matches** `prod.eu.frontend`. Tags declared directly on the deployed instance (`#gamma` in the `instanceOf` body) belong to the instance's own tag set and are visible to `source.tag` predicates just like any other tag.

**Tag-inheritance rule for deployment instances:** A deployed instance's resolved tag set is the **union** of two sources:
1. Tags declared directly on the `instanceOf` body (own tags, e.g. `#gamma`).
2. Tags inherited from the referenced logical model element (e.g. `#next` from `frontend`).

When a `where source.tag is #TAG` (or `target.tag`) filter is evaluated in a deployment view, LikeC4 checks this merged union. There is no distinction between own and inherited tags at filter time — both are treated equally. This mirrors how the deployment model inherits relationships from the logical model: the deployment layer augments but does not discard logical-model properties.
