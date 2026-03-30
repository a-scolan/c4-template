where source.tag is #next: matches
where source.tag is #gamma: matches
where source.tag is #missing: does not match

Deployment-instance tags are cumulative with the logical element tags, so filters can match both inherited logical tags like `#next` and instance-specific tags like `#gamma`.