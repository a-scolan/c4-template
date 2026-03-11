## Diagnostic racine

1. **Commencer par la taxonomie officielle** : relire `projects/shared/spec-*.c4` puis lancer `read-project-summary` sur le projet visé. Ce sont les deux sources à comparer avant toute correction.
2. **Comparer le token exact demandé** avec la taxonomie valide : nom complet, casse, niveau C4 et type de relation. Exemple classique : `Container_Api` ≠ `ContainerAPI`, `calls` ≠ `call`.
3. **Séquence de confirmation avant correction** :
   - confirmer l’ID de projet avec `list-projects` ;
   - relire le `read-project-summary` ;
   - vérifier `likec4.config.json` et `include.paths` ;
   - relire un exemple valide dans le projet courant ;
   - seulement ensuite corriger le kind ou la relation.
4. **Fallback si le résumé projet paraît incohérent** : rerun `read-project-summary` avec l’ID explicite, compare la liste `sources`, puis arrête l’édition si les includes ou fichiers chargés ne correspondent pas à ce que tu attends.
