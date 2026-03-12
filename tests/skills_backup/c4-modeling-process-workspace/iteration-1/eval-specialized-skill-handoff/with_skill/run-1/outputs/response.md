Non : ce skill **ne doit pas tout détailler lui-même**.

Son bon rôle est celui d’un **skill d’orchestration** :
- confirmer que le **C2 est assez stable**
- dire que la suite peut être :
  - `create-sequence-view` pour le **scénario nominal utilisateur**
  - `model-deployment-infrastructure` pour l’**infra de prod**
- éventuellement renvoyer vers `design-view` pour les vues et `test-model` pour la validation finale

En bref : **ordre, critères de passage, handoff explicite** — mais **pas** toutes les règles fines de déploiement et de dynamique. Sinon, le skill devient un couteau suisse un peu trop bavard.
