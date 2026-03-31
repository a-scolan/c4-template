`where source.tag is #next`: matches
`where source.tag is #gamma`: matches
`where source.tag is #missing`: does not match
Deployment-instance tags are cumulative, so `prod.eu.frontend` has both the logical tag `#next` inherited from `frontend` and its own added tag `#gamma`.