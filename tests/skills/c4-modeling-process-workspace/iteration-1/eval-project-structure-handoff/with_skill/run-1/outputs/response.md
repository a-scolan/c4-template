## Ordre conseillé

1. **`understand-project-structure` d’abord**  
   Reprends le contexte du workspace : projet actif, `likec4.config.json`, `spec-*.c4`, kinds/relations/tags autorisés, vues C1/C2/C3 existantes.

2. **Vérifie que le C1 est clair**  
   Une bonne vue C2 zoome sur **un système déjà bien délimité**.  
   Si la frontière du système est floue, reviens au C1 avant d’aller plus loin.

3. **`create-element`**  
   Modélise ou ajuste les **containers** du système.  
   Pense “frontières runtime/déployables”, pas “dossiers/classes”.

4. **`create-relationship`**  
   Relie les containers avec des types explicites (`calls`, `reads`, `writes`, `async`, `uses`) et des libellés courts.

5. **`design-view`**  
   Crée la vue dans `views 'C2'` en incluant :
   - le **système parent**
   - les **containers ciblés**
   - les **voisins entrants/sortants**  
   Règle d’or : **parent + focus + neighbors**.

6. **`test-model`**  
   Valide les références, les kinds, les relations et le rendu avant de terminer.

## Skills complémentaires à appeler

### Pour ton cas, les essentiels

- `understand-project-structure`
- `create-element`
- `create-relationship`
- `design-view`
- `test-model`

### Seulement si le besoin apparaît ensuite

- `customize-view` : pour affiner layout, style, navigation
- `create-sequence-view` : si tu dois montrer un flux temporel
- `model-deployment-infrastructure` : si la topologie de déploiement devient importante

## Raccourci mental

**Comprendre le projet → stabiliser C1 → modéliser les containers → relier → dessiner la C2 → valider.**

Et surtout : **ne saute pas directement au C3** — il doit “mériter” son existence.
