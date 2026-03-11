D’abord, **cadrer le dépôt** : confirmer le projet actif avec `list-projects`, relire son `read-project-summary`, puis vérifier `likec4.config.json`, les `projects/shared/spec-*.c4`, le modèle existant et les vues existantes.

Une fois ce socle fixé, le skill qui doit prendre la main est **`c4-modeling-process`**.

### Ce que `understand-project-structure` doit figer avant handoff

- le **projet réellement ciblé** ;
- les **sources of truth** à utiliser ;
- les **kinds / relations / tags** valides ;
- les **fichiers à modifier** ;
- l’état courant des niveaux **C1 / C2 / C3** déjà présents.

### Rôle de chaque skill

- **`understand-project-structure`** : cadrage workspace et validation de contexte avant édition.
- **`c4-modeling-process`** : orchestration du travail top-down **C1 → C2 → C3**, puis handoff éventuel vers Dynamic / Deployment.
