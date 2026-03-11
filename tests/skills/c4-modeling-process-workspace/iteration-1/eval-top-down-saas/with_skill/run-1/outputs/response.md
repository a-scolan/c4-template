La bonne démarche LikeC4 pour partir de zéro sur un SaaS, c’est :

1. **(Si besoin) cadrer le projet** — comprendre les règles du workspace, les types d’éléments autorisés et l’organisation des vues.  
   *Optionnel si tout est déjà clair.*

2. **C1 — Contexte** **(obligatoire)**  
   Définir la **frontière du produit**, les **acteurs** et les **systèmes externes**.  
   But : répondre à **“qu’est-ce que le système et dans quel environnement il vit ?”**  
   **Ne pas** mettre de séquence temporelle ici.

3. **C2 — Conteneurs** **(obligatoire)**  
   Découper le SaaS en **blocs d’exécution** : webapp, API, worker, base, broker, etc.  
   But : répondre à **“quelles briques runtime le font fonctionner ?”**

4. **C3 — Composants** **(optionnel)**  
   N’ouvrir l’intérieur **que des conteneurs qui le méritent** : complexes, risqués, centraux.  
   Inutile de faire un C3 pour chaque conteneur.

5. **Vues dynamiques / Use Cases** **(optionnel)**  
   À ajouter **après C2**, seulement si l’**ordre des interactions** compte : parcours utilisateur, async, erreurs, validations.  
   But : montrer **le déroulé dans le temps**.

6. **Vues de déploiement** **(optionnel)**  
   À ajouter **après que la structure est stable**, si la **topologie d’exécution** compte : environnements, zones, VM, apps, `instanceOf`.  
   But : répondre à **“où ça tourne ?”**

7. **Validation finale** **(obligatoire)**  
   Vérifier que le modèle est **cohérent, lisible et rendable**.

### En résumé

**Ordre recommandé :**  
**C1 → C2 → C3 (si utile) → Dynamique (si utile) → Déploiement (si utile) → Validation**

### Ce qui est optionnel

- le cadrage initial **si** le workspace est déjà maîtrisé
- **C3**
- les vues **Use Cases**
- les vues **Deployment**

### Règle d’or

Ne pars **ni des classes, ni des frameworks, ni de l’infra**.  
Pars du **périmètre du système**, puis des **conteneurs runtime**, puis du **détail interne seulement là où il apporte vraiment de la valeur**.
