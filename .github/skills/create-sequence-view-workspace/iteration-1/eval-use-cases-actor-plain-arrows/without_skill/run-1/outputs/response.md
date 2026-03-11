Je partirais plutôt sur une vue classique :

```likec4
views 'C2' {
  view login_flow {
    user -[https]-> mySystem.webapp
    mySystem.webapp -[calls]-> mySystem.api
    mySystem.api -[sql]-> mySystem.database
  }
}
```

Ça montre déjà les échanges principaux.