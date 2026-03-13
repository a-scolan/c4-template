Start with a `Deployment` view, not a C2, because `SecZone` is first and foremost infrastructure topology. A clean starting point is:

views 'Deployment' {
  deployment view prod_secZone {
    title 'Production SecZone'
    include production
    include production.secZone
    include production.secZone.bastionVm
    include production.secZone.firewallVm
    include production.secZone.adminServiceVm
    include production.secZone.sharedServiceVm
  }
}

Only add a C2 if you later discover a separate structural question, such as which application containers live behind `SecZone` or which systems and neighbors need a logical view. Do not create the extra C2 by default just because the zone exists. If you need to formalize how `SecZone` fits with DMZ/App/Data boundaries or capture security-tier organization, hand that part to `structure-deployment-tiers`. If you want stronger visual emphasis afterward, that is a `customize-view` pass, not a reason to expand the structural scope.
