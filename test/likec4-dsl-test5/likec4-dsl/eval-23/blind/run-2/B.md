where source.tag is #next: matches
where source.tag is #gamma: matches
where source.tag is #missing: does not match

Tag matching is cumulative for deployment instances, so inherited logical tags and instance-level tags are both considered rather than being replacement-only or isolated.# Eval-23 Response

`where source.tag is #next`: matches
`where source.tag is #gamma`: matches
`where source.tag is #missing`: does not match

Deployment-instance tags are **cumulative**: the instance inherits all tags from its logical element (`frontend` contributes `#next`) and merges them with any tags declared directly on the instance (`#gamma`), so both sets are visible to tag filters.
