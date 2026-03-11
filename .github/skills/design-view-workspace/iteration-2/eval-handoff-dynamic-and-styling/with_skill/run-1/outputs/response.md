Je découperais le besoin en trois rôles bien séparés :

- Le **parcours temporel** d'upload pas à pas relève de `create-sequence-view`, dans `views 'Use Cases'`.
- La **mise en avant visuelle** (couleurs, opacité, navigation) relève ensuite de `customize-view`.
- `design-view`, lui, sert surtout à cadrer une **vue structurelle compagnon** — par exemple une C2 ou une C3 du service d'upload avec parent, focus et voisins.

Autrement dit : ne mélange pas le flow dynamique et le styling avancé dans `design-view` ; utilise-le pour poser le contexte statique qui accompagnera la séquence.