Yes. `include prod.eu -> prod.db where source.tag is #next` will match a relation whose actual source is `prod.eu.frontend`, because a deployed instance inherits the tags of the logical element referenced by `instanceOf`. Since logical `frontend` has `#next`, the deployed instance `prod.eu.frontend` is treated as having `#next` too.

Yes for `#gamma` as well. If the deployment instance itself adds `#gamma`, then `where source.tag is #gamma` also matches relations originating from `prod.eu.frontend`.

Rule: for deployment instances, the effective tags are additive: they include the tags from the referenced logical element (`instanceOf frontend`) plus any tags declared directly on the deployed instance. So in your example, `prod.eu.frontend` effectively has both `#next` and `#gamma`, and either predicate can match when the relation source is that deployment instance.
