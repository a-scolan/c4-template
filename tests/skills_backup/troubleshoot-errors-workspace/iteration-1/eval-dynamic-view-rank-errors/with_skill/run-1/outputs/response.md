Il y a deux problèmes conceptuels :
- En dynamic view, un parent ne doit pas appeler son propre child. Il faut montrer l’acteur ou l’élément externe qui accède directement au composant utile.
- `rank same` ne fonctionne qu’avec des éléments ayant le même parent ; `user` et `mySystem.api` ne vivent pas dans le même contexte.

Corrige donc la séquence pour partir de l’acteur pertinent, puis supprime ou scinde la contrainte de rang pour ne garder que des siblings.
