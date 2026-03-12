Après un switch de projet, repars de zéro sur le contexte :

1. **`list-projects`** pour revalider les IDs réellement disponibles (`template-project`, `spec-showcase`, etc.).
2. **`read-project-summary`** sur le projet ciblé pour recharger éléments, kinds, relations, tags et sources incluses.
3. **Relire les specs partagées** avant d’éditer une C3 : au minimum `projects/shared/spec-components.c4`, `spec-containers.c4` et `spec-global.c4`.
4. **Relire le parent réel de la vue C3** (container ciblé, système parent, vues existantes) avant de toucher le fichier.
5. Seulement après ça, éditer la vue.

### Risques évités

- **Contexte obsolète** : tu crois encore être dans l’ancien projet.
- **Kind ou relation invalide** : tu réutilises une taxonomie non revalidée.
- **Mauvais parent C3** : tu détailles le mauvais container ou un container qui n’existe pas dans le projet courant.
- **Références cassées** : la vue pointe vers des éléments du mauvais projet.
