Je vérifie la structure LikeC4 du repo et les specs partagées pour te répondre selon les règles réelles du workspace, pas au doigt mouillé.

J’ai trouvé les configs LikeC4, mais pas encore la taxonomie réelle. Je lis maintenant les specs partagées et un exemple de projet pour voir la règle locale sur les kinds.

Je vois déjà le pattern: le repo a une taxonomie de `Container_*` partagée et réutilisée, pas des kinds métier jetables. Je vais confirmer avec le cheatsheet et les guidelines du skill de création d’éléments.

J’ai la règle locale: ici, les kinds sont une taxonomie partagée de style/sémantique, pas des noms de rôles métier par service. Je finalise la réponse avec la marche à suivre avant toute création de kind.

Plutôt **non** dans ce repo.

La règle locale: les `kind` décrivent une **taxonomie partagée et réutilisable** (`projects/shared/spec-*.c4`), pas un rôle métier one-off. Ici on réutilise des kinds génériques/stylés comme `Container_Api`, `Container_ProcessingServer`, `Container_Queue`, puis on met le métier dans le **nom** et la **description**. Exemple valide: `uploadApi = Container_Api 'Upload API'`.

Avant d’ajouter un nouveau kind:

1. Vérifie le projet actif et le résumé projet.
2. Relis `likec4.config.json` + `projects/shared/spec-*.c4` / `SPEC_CHEATSHEET.md`.
3. Décide le niveau C4: si c’est interne à un service, fais plutôt un `Component 'Upload Orchestrator'`.
4. N’ajoute un kind que s’il manque une **catégorie technique réutilisable** pour plusieurs cas, avec accord explicite.
