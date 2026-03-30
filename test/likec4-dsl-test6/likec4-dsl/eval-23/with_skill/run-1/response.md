where source.tag is #next: matches
where source.tag is #gamma: matches
where source.tag is #missing: does not match

Deployment-instance tags are cumulative: the instance keeps tags inherited from the logical element and adds its own deployment tags, rather than replacing them or keeping them isolated.