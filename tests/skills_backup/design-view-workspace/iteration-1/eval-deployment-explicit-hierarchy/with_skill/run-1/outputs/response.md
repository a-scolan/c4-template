Pour une vue d’infrastructure conforme au repo, utilise `views 'Deployment'`, un `deployment view`, puis liste l’environnement, les zones et chaque VM explicitement.

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

Évite `production.*` / `**` et reste au niveau VM dans cette vue.
