Pars d'une vue structurelle existante et ajoute une couche de style, sans supprimer le contexte :

```likec4
view api_focus {
  include *

  style * { color muted; opacity 20% }
  style api, geo_api, api_container { color primary; opacity 100% }
}
```

Ici, on reste sur la palette partagée (`muted`, `primary`) et on atténue le bruit au lieu de masquer complètement le contexte parent.