Je partirais sur quelque chose de rapide :

```likec4
views 'Deployment' {
  deployment view prod_overview {
    include production.*
    include production.appTier.**
  }
}
```

Ça donne tout de suite une vue large de la prod.