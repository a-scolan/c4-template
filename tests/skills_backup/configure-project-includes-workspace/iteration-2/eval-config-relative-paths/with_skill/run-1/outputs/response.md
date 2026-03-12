Pars du template et garde les champs de base : `$schema`, `name`, `title`, `include.paths` et `imageAliases`.

Depuis `projects/payments/`, garde des chemins relatifs :
- specs partagées : `../shared`
- alias images : `@` → `../shared/images/`

Exemple minimal :
```json
{
  "$schema": "https://likec4.dev/schemas/config.json",
  "name": "payments",
  "title": "Payments Architecture",
  "include": { "paths": ["../shared"] },
  "imageAliases": { "@": "../shared/images/" }
}
```

Fais une modif ciblée du config et évite les chemins absolus.
