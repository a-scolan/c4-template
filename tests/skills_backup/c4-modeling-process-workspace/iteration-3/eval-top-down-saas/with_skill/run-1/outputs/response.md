Je charge la guidance de modélisation C4 pour te donner un ordre de conception propre dès le départ, avec ce qui est requis vs optionnel.

La bonne démarche LikeC4 est :

1. **Contexte projet** — comprendre la structure du workspace, les types d’éléments, relations et conventions. **Requis**.  
2. **C1 / System Context** — définir la frontière du produit, les acteurs et systèmes externes. **Requis**.  
3. **C2 / Containers** — découper le SaaS en blocs d’exécution réels : webapp, API, DB, workers, etc. **Requis**.  
4. **C3 / Components** — détailler seulement les conteneurs complexes ou critiques. **Optionnel**.  
5. **Dynamic views / Use Cases** — ajouter les flux temporels importants. **Optionnel**.  
6. **Deployment views** — modéliser environnements, zones, VMs/apps. **Optionnel**.  
7. **Validation** — vérifier cohérence et rendu. **Requis**.

Règle clé : **top-down uniquement — C1 → C2 → C3**, puis dynamique et déploiement si utile.
