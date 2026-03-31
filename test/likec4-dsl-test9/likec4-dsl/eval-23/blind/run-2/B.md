where source.tag is #next: matches
where source.tag is #gamma: matches
where source.tag is #missing: does not match

Deployment-instance tags are cumulative: the instance keeps the logical element’s tags and adds its own, so `prod.eu.frontend` matches both `#next` and `#gamma`.