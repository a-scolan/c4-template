Je partirais sur un découpage clair en **tiers** :

- **`Dmz`** : point d'entrée Internet, TLS, API gateway, éventuel web server
- **`AppTier`** : services métier synchrones exposés en interne
- **`ProcTier`** : traitement asynchrone, donc **RabbitMQ** + **worker(s)**
- **`DataTier`** : stockage persistant, donc **MongoDB** + **MinIO**
- **`SecZone`** *(optionnel)* : monitoring, métriques, logs
- **`InfraZone`** *(optionnel)* : backup / DR si tu veux le montrer explicitement

Règles réseau essentielles :
- **Internet → `Dmz`** uniquement sur 443
- **`Dmz` → `AppTier`** pour router les appels internes
- **`AppTier` → `ProcTier`** pour publier vers la file
- **`ProcTier` → `DataTier`** pour persister les résultats
- **`DataTier`** reste **interne seulement** : jamais exposé à Internet

Le point clé est de séparer les responsabilités : le synchrone en `AppTier`, l'async en `ProcTier`, la persistance en `DataTier`, avec monitoring isolé si besoin dans `SecZone`.