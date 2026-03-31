where source.tag is #next: matches
where source.tag is #gamma: matches
where source.tag is #missing: does not match

Deployment-instance tags are cumulative: an instance matches both its own tags and the logical tags inherited from the element referenced by `instanceOf`.