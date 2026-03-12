Tu peux enrichir la vue en ajoutant l'URL dans la description et en pointant la webapp vers une future vue détaillée :

```likec4
view c2_containers {
  description 'Voir https://docs.internal/spec'

  include mySystem.webapp with {
    navigateTo webapp_deep_dive
  }

  include mySystem.api
}
```

Tu pourras créer `webapp_deep_dive` plus tard si besoin.