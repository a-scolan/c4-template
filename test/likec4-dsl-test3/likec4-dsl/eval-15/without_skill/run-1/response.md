En LikeC4 :

- `payment.api` ✅ **valide comme identifiant qualifié (FQN)** : chaque segment (`payment`, `api`) est un identifiant valide, séparé par `.`.
- `1backend` ❌ **invalide** : un identifiant ne peut pas commencer par un chiffre.
- `payment_api` ✅ **valide** : lettres + underscore autorisés.
- `payment-api` ❌ **invalide** : `-` n’est pas autorisé dans un identifiant (interprété comme opérateur/séparateur, pas comme nom).

Réécriture des invalides en conservant le sens :

- `1backend` → `backend1`
- `payment-api` → `payment_api`
