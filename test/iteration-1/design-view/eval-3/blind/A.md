Start with a Deployment view.

A new production `SecZone` is primarily an infrastructure concern, so the cleanest first artifact is a deployment view that shows the zone boundary and the hosted nodes:

```likec4
views 'Deployment' {
  deployment view production_seczone {
    title 'Production SecZone'

    include Prod
    include Prod.SecZone
    include Prod.SecZone.firewallVm
    include Prod.SecZone.bastionVm
    include Prod.SecZone.serviceAVm
    include Prod.SecZone.serviceBVm

    autoLayout LeftRight
  }
}
```

Add a C2 view only if you have a separate stakeholder question about logical service relationships inside `SecZone`—for example, which service calls which, or which data store each service owns. If the goal is simply to show the secured production zone, the deployment view is enough.

Keep zone boundaries and security organization in the deployment hierarchy first, and treat any later visual emphasis as a separate styling pass rather than part of the view-design decision.
