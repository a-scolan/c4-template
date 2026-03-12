Pour une vraie C2 du template, garde `view index` à la racine et complète la vue dans `views 'C2'` :

```likec4
views 'C2' {
  view c2_containers {
    title 'Containers'

    include user
    include mySystem
    include mySystem.*
    include -> mySystem.*
    include mySystem.* ->
    include emailService

    include mySystem.webapp with {
      navigateTo c2_webapp_details
    }

    rank source { user }
    rank sink { mySystem.database, emailService }
  }
}
```

Le cadrage `design-view`, ici, c'est bien **parent + focus + neighbors** ; le styling avancé reste pour `customize-view`.