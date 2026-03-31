where source.tag is #next: matches
where source.tag is #gamma: matches
where source.tag is #missing: does not match
Deployment-instance tags are cumulative with the logical element's tags, so `source.tag` can match either inherited logical tags or tags added on the instance itself.