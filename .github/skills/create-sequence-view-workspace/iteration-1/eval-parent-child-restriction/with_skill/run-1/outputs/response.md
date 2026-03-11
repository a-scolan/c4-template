Évite `api_container -> api_container.auth_component` : dans une vue dynamique, on ne montre pas un parent appelant son propre child.

Corrige plutôt ainsi :

```likec4
views 'Use Cases' {
  dynamic view auth_flow {
    title 'Authentication'

    person_external -> api_container.auth_component 'Starts authentication'
    api_container.auth_component -> directory 'Validate credentials'
    api_container.auth_component -> component_database 'Read user data'
  }
}
```

Ici, l'acteur cible directement le composant et toutes les interactions restent en `->` simples.