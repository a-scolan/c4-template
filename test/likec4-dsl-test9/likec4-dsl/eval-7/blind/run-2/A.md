Voici un `detail` view qui fait exactement cela :

```likec4
view backend-overview of cloud.backend {
  include *
}

detail view backend-detail extends backend-overview {
  include api
  include _ -> cloud.backend
}
```

## Explication

- `extends backend-overview` réutilise le contenu du view de base.
- `include api` fonctionne grâce à **l’héritage de portée** : comme le view parent est `of cloud.backend`, le nom `api` est résolu relativement à cette portée, donc il signifie `cloud.backend.api`.
- `include _ -> cloud.backend` ajoute toutes les **relations entrantes** vers `cloud.backend` depuis le reste du modèle, via un **prédicat de relation** :
  - `_` = n’importe quelle source
  - `-> cloud.backend` = toute relation dont la cible est `cloud.backend`

## Ce que signifie l’héritage de portée ici

Le view étendu conserve le même contexte de résolution que `backend-overview`, à savoir `cloud.backend`. Donc, dans le `detail view`, vous pouvez écrire des noms relatifs comme `api` au lieu du FQN complet `cloud.backend.api`.

Autrement dit, la portée du parent est héritée par l’enfant, ce qui rend le DSL plus court et plus lisible.