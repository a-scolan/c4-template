where source.tag is #next: matches
where source.tag is #gamma: matches
where source.tag is #missing: does not match

Deployment-instance tags are cumulative, so filters can match tags inherited from the logical element and tags added on the instance itself.# Eval-23 Response

`where source.tag is #next`: matches
`where source.tag is #gamma`: matches
`where source.tag is #missing`: does not match

Deployment-instance tags are **cumulative**: a deployed instance inherits all tags from its logical element (`#next` from `frontend`) and any tags declared on the instance itself (`#gamma`) are added on top, so the effective tag set is the union of both.
