Non : ce skill **ne doit pas tout détailler lui-même**.

Avec un **C2 déjà stable**, `c4-modeling-process` sert surtout de **cadre d’orchestration** : il décide quand passer à l’étape suivante, puis renvoie le détail aux bons skills.

Dans ton cas :
- **infra de prod** → `model-deployment-infrastructure`
- **scénario nominal utilisateur** → `create-sequence-view`

Rappel : **Deployment** et **Dynamic** viennent **après le noyau C1/C2**, de façon ciblée et seulement quand ils apportent une vraie valeur.
