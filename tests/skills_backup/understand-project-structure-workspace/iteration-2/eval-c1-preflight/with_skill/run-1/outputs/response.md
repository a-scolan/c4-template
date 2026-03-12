## Préflight

- **Projet à confirmer avant edit** : lance `list-projects`, puis `read-project-summary` sur le projet ciblé. Dans ce dépôt, l’édition d’un vrai système vise en général `template-project` (`projects/template/`), pas `spec-showcase` qui sert surtout de référence.
- **Sources of truth** :
  - `projects/template/likec4.config.json`
  - `projects/shared/spec-context.c4`, `spec-containers.c4`, `spec-components.c4`, `spec-global.c4`
  - `projects/template/system-model.c4`
  - `projects/template/system-views.c4`
  - le `read-project-summary` du projet actif

## Taxonomie à ne pas inventer

Pour `template-project`, tu peux déjà vérifier des exemples valides :
- **kinds** : `Container_Api`, `Container_Webapp`, `Container_Database`
- **relations** : `calls`, `reads`, `writes`, `async`, `uses`
- **tags** : `Container`, `Api`, `Database`, `Webapp`, `System`, `External`

## Plan avant modification

1. **C1** — confirmer que le nouveau container reste bien dans la frontière `mySystem`, avec `user` et `emailService` comme contexte existant.
2. **C2** — ajouter le nouveau `Container_Api` dans `projects/template/system-model.c4`, puis relier proprement `mySystem.webapp`, `mySystem.database` et/ou `emailService`.
3. **C2 views** — mettre à jour `projects/template/system-views.c4` (`c2_containers` ou vue sœur).
4. **C3** — n’ouvrir un détail interne que si ce nouvel API devient complexe ; sinon on s’arrête au C2.
