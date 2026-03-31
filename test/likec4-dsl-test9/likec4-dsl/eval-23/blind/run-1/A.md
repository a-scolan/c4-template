where source.tag is #next: matches
where source.tag is #gamma: matches
where source.tag is #missing: does not match
Deployment-instance tags are cumulative with the logical element tags, so the instance matches both inherited tags like `#next` and its own added tags like `#gamma`. 