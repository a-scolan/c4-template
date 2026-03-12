Je partirais sur une vue large pour aller vite :

```likec4
views 'Deployment' {
  deployment view prod_overview {
    include production.*
    include production.appTier.**
  }
}
```

On pourra préciser après si besoin.
