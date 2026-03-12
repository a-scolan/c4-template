Voici l’ordre recommandé pour partir de zéro sur un nouveau produit SaaS en LikeC4 :

1. **C1 — Contexte**  
   - Définir **la frontière du système**.  
   - Identifier les **acteurs** et **systèmes externes**.  
   - Ajouter les **relations externes**.  
   - Créer une **vue C1**.  
   - **Important :** la vue C1 reste **statique** ; pas de flux temporels ici.

2. **C2 — Conteneurs**  
   - Découper le SaaS en **unités d’exécution/déploiement** : UI web, API, worker, base, queue, etc.  
   - Documenter les **technologies**.  
   - Décrire les **relations entre conteneurs** (sync/async si utile).  
   - Créer une **vue C2** complète.

3. **C3 — Composants**  
   - Détailler **uniquement les conteneurs complexes ou critiques**.  
   - Modéliser des **groupes logiques de code**, pas des classes.  
   - Garder le **contexte du conteneur parent** dans la vue C3.  
   - 👉 **Optionnel** : à faire seulement si le niveau de détail apporte de la valeur.

4. **Déploiement**  
   - Montrer **où tourne** le système : environnements, zones, VM, apps, instances.  
   - Créer une **vue de déploiement** si nécessaire.  
   - 👉 **Optionnel**.

5. **Dynamique / Use Cases**  
   - Documenter les **flux métier importants** ou scénarios clés.  
   - Mettre ces vues dans **`Use Cases`**, pas dans C1.  
   - En général, **2 à 5 vues** suffisent.  
   - 👉 **Optionnel**.

6. **Validation finale**  
   - Vérifier que chaque élément, relation et vue est bien nommé et décrit.  
   - Lancer la validation du modèle.

### En bref

- **Obligatoire dans l’ordre** : **C1 → C2 → C3**  
- **C3** : **optionnel / sélectif**  
- **Déploiement** : **optionnel**  
- **Dynamique / Use Cases** : **optionnel**  
- **Toujours finir par la validation**

La logique est simple : **on conçoit de haut en bas**, jamais l’inverse.
