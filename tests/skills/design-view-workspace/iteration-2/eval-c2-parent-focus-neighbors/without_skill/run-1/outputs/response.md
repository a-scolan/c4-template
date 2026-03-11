Je ferais une vue simple dans le dossier C2 :

```likec4
views 'C2' {
  view c2_containers {
    title 'Containers'

    include user
    include mySystem.*
    include emailService
  }
}
```

Ça donne déjà les blocs principaux, quitte à détailler après.