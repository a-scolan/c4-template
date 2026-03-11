Ajoute une vue dynamique dans `views 'Use Cases'` pour montrer l'ordre réel des interactions :

```likec4
views 'Use Cases' {
  dynamic view login_flow {
    title 'Login'

    user -> mySystem.webapp 'Opens login form'
    mySystem.webapp -> mySystem.api 'POST /login'
    mySystem.api -> mySystem.database 'Read user record'
    mySystem.api -> emailService 'Send login alert'
    mySystem.api -> mySystem.webapp 'Session established'
  }
}
```

Ici, l'acteur initiateur `user` est bien en premier et toutes les interactions restent sur des flèches simples `->` avec des labels d'action.