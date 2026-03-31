where source.tag is #next: matches
where source.tag is #gamma: matches
where source.tag is #missing: does not match
Deployment-instance tags are cumulative, so the instance matches both its own deployment tag(s) and the tag(s) inherited from the logical element rather than replacing or isolating them.
