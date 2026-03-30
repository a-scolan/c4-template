where source.tag is #next: matches
where source.tag is #gamma: matches
where source.tag is #missing: does not match

Deployment-instance tags are **cumulative**: the instance inherits all tags from its logical element and merges them with any tags declared directly on the instance, so both `#next` (from `frontend`) and `#gamma` (added by `prod.eu.frontend`) are present on the deployed instance at the same time.
