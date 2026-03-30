where source.tag is #next: matches
where source.tag is #gamma: matches
where source.tag is #missing: does not match

Deployment-instance tags are cumulative with logical element tags, so both inherited (`#next`) and instance-added (`#gamma`) tags match while absent tags do not.