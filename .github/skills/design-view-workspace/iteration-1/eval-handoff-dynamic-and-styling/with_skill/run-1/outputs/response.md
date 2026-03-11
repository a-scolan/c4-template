Ici le besoin est mixte :

- le **parcours temporel** doit passer par `create-sequence-view`
- la **mise en forme** (couleurs, layout, navigation) relève ensuite de `customize-view`

`design-view` sert surtout à cadrer une vue structurelle compagnon — C2 ou C3 — avec **parent + focus + voisins**.
Donc je ferais :
1. la `dynamic view` d’upload via `create-sequence-view` dans `views 'Use Cases'` ;
2. si tu veux une vue statique de support, une C2/C3 via `design-view` ;
3. puis la finition via `customize-view`.
