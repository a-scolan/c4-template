The cleanest approach is to start with a Deployment view for `SecZone`, then add a C2 only if you later discover a separate logical-service question that the deployment view does not answer.

```likec4
deployment {
  Node_Environment Prod 'Production' {
    #Production

    Zone SecZone 'SecZone' {
      #Dmz #Security

      Infra_Fw perimeterFw 'Perimeter Firewall'
      Node_Vm bastionVm 'Bastion VM'
      Node_Vm servicesVm 'Dedicated Services VM'
    }
  }
}

views 'Deployment' {
  deployment view seczone_overview {
    title 'Production SecZone'

    include Prod
    include Prod.SecZone
    include Prod.SecZone.perimeterFw
    include Prod.SecZone.bastionVm
    include Prod.SecZone.servicesVm
  }
}
```

That should be the first artifact, because `SecZone` is primarily an infrastructure boundary.

Do not create a detailed C2 by default. Add a C2 only when you have a distinct need to explain logical container relationships inside the zone, such as which service talks to which or which data store each service owns.

If you need to organize zone boundaries, tiers, or security-rule structure, use `structure-deployment-tiers`. If you only want stronger visual emphasis after the structure is settled, use `customize-view` only for the visual treatment.