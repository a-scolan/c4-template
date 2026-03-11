Pour rester conforme aux conventions du repo, pose la vue dans `views 'Deployment'` et liste l'infrastructure explicitement :

```likec4
views 'Deployment' {
  deployment view prod_overview {
    title 'Production Infrastructure'

    include production
    include production.dmzTier
    include production.appTier
    include production.dataTier

    include production.dmzTier.webVm
    include production.appTier.apiVm
    include production.appTier.workerVm
    include production.dataTier.dbVm

    autoLayout TopBottom
  }
}
```

L'important, ici, c'est la hiérarchie explicite **environnement → zones → VMs**, sans wildcard et sans descendre plus bas que la VM.