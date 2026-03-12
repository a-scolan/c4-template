Tu peux enrichir la vue C2 avec un bloc très ciblé :

```likec4
view c2_containers {
  link https://docs.internal/spec 'Internal Specification'

  include mySystem.webapp with {
    navigateTo c2_webapp_details
  }
}
```

Le `navigateTo` vise un view ID déjà présent dans le template, donc le drill-down reste stable et on reste bien dans le périmètre de la personnalisation.