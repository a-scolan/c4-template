Tu peux garder l'idée en la rendant plus directe :

```likec4
views 'Use Cases' {
  dynamic view auth_flow {
    title 'Authentication'

    api_container -> api_container.auth_component 'Dispatch auth'
    api_container.auth_component -> directory 'Check LDAP'
  }
}
```

Ça montre bien que le conteneur délègue ensuite au composant d'authentification.