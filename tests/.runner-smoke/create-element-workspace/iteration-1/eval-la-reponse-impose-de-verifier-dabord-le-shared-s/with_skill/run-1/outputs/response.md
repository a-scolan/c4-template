Je vérifie rapidement les règles du workspace LikeC4 et les kinds déjà définis pour te répondre selon ce repo, pas en théorie générale.

J’ai trouvé le workspace. Je lis maintenant la config et les specs partagées pour voir si ce repo encourage des kinds “par métier” ou plutôt des kinds génériques + description/tags.

Je vois déjà un signal fort: les kinds `Container_*` existants sont des catégories réutilisables et stylées, pas des noms de services métier. Je cherche la règle explicite dans les skills/specs pour te donner la bonne recommandation.

J’ai assez d’indices: ce repo pousse vers des kinds partagés, génériques et réutilisables. Je vérifie juste les tags existants utiles pour un service d’upload/orchestration avant de conclure quoi utiliser à la place.

Non, **pas en première intention** dans ce repo.

La règle ici est: **on réutilise d’abord les kinds partagés de `projects/shared/spec-*.c4`**. Les `Container_*` existants représentent des **catégories réutilisables/stylées** (`Container_Api`, `Container_ProcessingServer`, `Container_Queue`, etc.), pas des services métier “one-off”. Le skill `create-element` dit explicitement: **check shared spec first**, **avoid one-off custom kinds**, et **ask before introducing new kinds**.

Donc pour un service d’upload, préfère probablement:

- `Container_Api 'Upload Orchestrator'`
- ou `Container_ProcessingServer 'Upload Orchestrator'`

…puis exprime le métier via `title`, `description`, `technology`, et éventuellement des tags existants pertinents.

**Avant d’ajouter un nouveau kind**:
1. lire `projects/shared/spec-containers.c4`
2. vérifier les kinds/tags disponibles
3. confirmer qu’aucun kind existant ne convient
4. si nécessaire, proposer un **kind générique réutilisable** dans la shared spec, pas un kind spécifique upload.
