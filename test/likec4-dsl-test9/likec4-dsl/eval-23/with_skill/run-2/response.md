where source.tag is #next: matches
where source.tag is #gamma: matches
where source.tag is #missing: does not match
Deployment-instance tags are cumulative: a deployment instance keeps the logical element’s tags and adds its own, so `prod.eu.frontend` has both `#next` and `#gamma`.
