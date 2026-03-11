Voici un bloc de personnalisation sobre pour `c2_containers` :

```likec4
view c2_containers {
  include mySystem.webapp with {
    navigateTo c2_webapp_details
  }

  rank source { user }
  rank sink { mySystem.database, emailService }
  autoLayout LeftRight
}
```

Je ne touche ni à la structure de base ni à la palette ; ici on reste sur **layout + navigation**.