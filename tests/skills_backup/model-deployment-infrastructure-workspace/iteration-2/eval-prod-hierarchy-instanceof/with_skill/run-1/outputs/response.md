Pour ce besoin, garde une hiérarchie fixe et explicite : **Environment → Zone → VM → Node_App**.

1. **Environment** : crée d'abord l'environnement, par exemple `Prod`.
2. **Zone** : place ensuite les segments réseau ou tiers utiles sous cet environnement.
3. **VM** : dans chaque zone, ajoute les `Node_Vm` qui portent l'infrastructure (`ProdApigwVm`, `ProdUploadVm`, `ProdWorkerVm`, `ProdDatabaseVm`).
4. **Node_App** : dans chaque VM, ajoute un `Node_App` relié au modèle logique avec `instanceOf` vers le container concerné.

Pour relier le déploiement au modèle, utilise donc `instanceOf` sur chaque `Node_App`. Les relations applicatives sont **héritées automatiquement** depuis le modèle logique : tu ne recopies pas les relations de déploiement à la main entre apps déployées. Tu n'ajoutes des relations explicites que pour des liens purement infra, comme monitoring, backup ou log shipping.

Pour les descriptions, reste riche et opérable :
- chaque **VM** a une table Markdown avec **`eth0` en premier**, puis OS, CPU, RAM, Disk, Port, RTO ;
- chaque **zone** documente VLAN, CIDR, gateway et règles réseau utiles.

En bref : **Environment → Zone → VM → Node_App**, `instanceOf` pour relier au modèle, relations héritées par défaut, descriptions infra détaillées.
