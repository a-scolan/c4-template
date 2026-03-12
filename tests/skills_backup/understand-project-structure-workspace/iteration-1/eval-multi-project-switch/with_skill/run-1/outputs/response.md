## Réponse with_skill

## Réponse concise

**Pour éviter les erreurs de contexte et éditer une vue C3 en sécurité :**

1. **Identifier le projet actif** — Utilisez `list-projects` pour confirmer quel projet est chargé. Dans un workspace multi-projet, utiliser le mauvais projet est la source d'erreur n°1.

2. **Recharger le contexte du projet** — Exécutez `read-project-summary` sur le projet ciblé pour obtenir:
   - La liste exacte des éléments C1/C2/C3 existants
   - Les kinds valides (component, service, module, etc.)
   - Les types de relations autorisées (calls, async, reads, writes, etc.)

3. **Valider les références des éléments** — Avant d'éditer la vue, vérifiez avec `search-element` que tous les composants C3 que vous voulez inclure existent dans le conteneur parent. Une référence manquante ou mal nommée provoque une erreur de rendu.

4. **Vérifier les specs partagées** — Consultez [projects/shared/spec-components.c4](projects/shared/spec-components.c4) et [projects/shared/spec-containers.c4](projects/shared/spec-containers.c4) pour confirmer les kinds autorisés au niveau C3.

5. **Lire la config du projet** — Vérifiez [projects/<projet>/likec4.config.json](projects/spec-showcase/likec4.config.json) pour voir quels fichiers modèles sont inclus — évite les fichiers manquants.

## Checklist d'auto-évaluation

- ✅ Lecture de la skill `understand-project-structure`
- ✅ Identification du contexte multi-projet (différents projects/ doivent être distingués)
- ✅ Vérifications MCP requises identifiées: `list-projects` → `read-project-summary` → `search-element`
- ✅ Fichiers clés de validation listés (spec-components.c4, likec4.config.json)
- ✅ Erreurs courantes évitées documentées (mauvais projet, références invalides, kinds non autorisés)
