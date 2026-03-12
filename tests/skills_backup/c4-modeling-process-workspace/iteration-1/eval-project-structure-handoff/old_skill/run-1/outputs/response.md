## Ordre conseillé

1. **Recadrer le workspace avant tout**  
   Appelle `understand-project-structure` pour identifier :
   - le projet actif,
   - les `spec-*.c4`,
   - les kinds/relations/tags autorisés,
   - les C1/C2/C3 déjà en place.  
   Bref : éviter le classique “je dessine vite, je casse tout” 😄

2. **Repartir du C1, même rapidement**  
   Avec `c4-modeling-process`, vérifie d’abord :
   - la frontière du système,
   - les acteurs,
   - les systèmes externes.  
   Une bonne C2 découle d’un C1 clair.

3. **Définir ou ajuster les conteneurs**  
   Appelle `create-element` pour poser les vrais conteneurs :
   - unités runtime,
   - déployables,
   - avec techno + description.

4. **Poser les bonnes relations**  
   Appelle `create-relationship` pour typer proprement les liens :
   - `calls`, `async`, `reads`, `writes`, `uses`,
   - avec labels courts et explicites.

5. **Construire la vue C2**  
   Appelle `design-view` pour faire une vue propre :
   - dans `views 'C2'`,
   - avec le **système parent**,
   - les **conteneurs ciblés**,
   - et leurs **voisins** (`include -> ...` / `... ->`).

6. **Valider avant de conclure**  
   Appelle `test-model` pour vérifier :
   - références,
   - relations,
   - rendu de la vue,
   - erreurs de structure/syntaxe.

## Skills complémentaires à appeler

- **Indispensables pour ton cas**
  - `understand-project-structure`
  - `create-element`
  - `create-relationship`
  - `design-view`
  - `test-model`

- **Seulement si besoin ensuite**
  - `customize-view` : si tu dois affiner style/layout/navigation
  - `create-sequence-view` : si on te demande aussi un flux métier/dynamique
  - `c4-modeling-process` : pour garder la discipline **C1 → C2 → C3**, sans sauter les étapes

En une phrase : **comprends d’abord le terrain, confirme le C1, modélise les conteneurs, relie-les, dessine la vue C2, puis valide.**
