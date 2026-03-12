Pour une vraie C2 du template, garde `view index` à la racine et mets la vue dans `views 'C2'`.

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

Le point clé ici, c’est **parent (`mySystem`) + focus (`mySystem.*`) + voisins**.
