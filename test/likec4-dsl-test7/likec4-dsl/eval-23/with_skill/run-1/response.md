where source.tag is #next: matches
where source.tag is #gamma: matches
where source.tag is #missing: does not match
Deployment-instance tags are cumulative, so an instance matches filters against both its own tags and the tags inherited from the logical element it comes from.