Non : ce skill **ne doit pas tout détailler lui-même**.

Avec un **C2 déjà prêt**, `c4-modeling-process` doit surtout servir de **guide d’orientation** : il dit **quand** passer au déploiement et au dynamique, puis **délègue les règles détaillées** à des skills spécialisés.

Dans ton cas :
- **Infra de prod** → s’appuyer sur le skill de **déploiement** (`model-deployment` dans l’ancienne version, aujourd’hui plutôt `model-deployment-infrastructure`)
- **Scénario nominal utilisateur** → s’appuyer sur **`create-sequence-view`**

Donc la bonne responsabilité est :
- `c4-modeling-process` = **cadre global + ordre des étapes + hand-off**
- skills spécialisés = **règles fines, conventions, contraintes, exemples détaillés**

Bref : **orchestrateur, pas encyclopédie**.
