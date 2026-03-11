## Réponse baseline (old_skill)

### Comment éviter les erreurs de contexte en workspace multi-projet

Quand tu changes de projet pour modifier une vue C3, le risque principal est de **mélanger les contextes** : référencer des éléments qui n'existent que dans l'ancien projet, ou utiliser des `kinds` et `relationships` non définis dans le projet cible.

**Checklist avant d'éditer :**

1. **Charger le contexte du nouveau projet** — Appelle `read-project-summary` du LikeC4 MCP pour :
   - Confirmer quels `kinds` sont valides
   - Obtenir les FQNs exacts des éléments C3 existants
   - Voir les `relationship` types disponibles

2. **Vérifier les éléments de ta vue** — Pour chaque élément dans la vue C3 :
   - Appelle `search-element` avec le FQN pour confirmer qu'il existe dans **ce projet**
   - Note le `kind` exact retourné

3. **Valider les relationships** — Avant d'ajouter/modifier une relation :
   - Appelle `find-relationships` pour voir quelles connexions existent déjà
   - Vérifie que le type de relationship (ex : `calls`, `async`, `reads`) est défini dans la spec du projet

4. **Tester le rendu** — Appelle `open-view` pour :
   - Confirmer que ta vue C3 se compile sans erreurs
   - Détecter les éléments manquants ou FQNs invalides **avant** de sauvegarder

## Auto-évaluation des vérifications effectuées

- ✓ Exploration du workspace multi-projet (`shared/`, `spec-showcase/`, `template/`)
- ✓ Vérification des instructions MCP dans copilot-instructions.md
- ✓ Identification des 3 MCP calls critiques : `read-project-summary`, `search-element`, `find-relationships`
- ✓ Listage de la séquence d'ordre logique (contexte → éléments → relations → rendu)
