Pour les éléments :

- `virusTotal` → `System_External`
- `scanApi` → `Container_Api` sous ton système

Puis découpe comme suit :

1. `create-element` pour déclarer `virusTotal` et `scanApi` avec les bons kinds partagés.
2. `create-relationship` pour poser les flèches.
3. `design-view` pour construire la vue C2.

Donc ici `create-element` reste centré sur les **déclarations d’éléments**, pas sur les relations ni sur la vue.