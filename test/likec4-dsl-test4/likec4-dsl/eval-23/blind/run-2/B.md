where source.tag is #next: matches
where source.tag is #gamma: matches
where source.tag is #missing: does not match

Deployment-instance tags are cumulative: a deployed instance inherits all tags from its logical element and merges them with its own instance-level tags, so `source.tag` filtering sees the union of both sets.
