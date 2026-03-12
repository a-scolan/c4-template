Les deux erreurs viennent de vraies contraintes de modélisation, pas d’un simple bug de syntaxe :
1. Dans une dynamic view, un parent ne doit pas “appeler” son propre child ; fais partir l’action de l’acteur ou d’un externe directement vers `mySystem.api`.
2. `rank same user, mySystem.api` casse si les éléments ne partagent pas le même parent ; cette contrainte ne sert qu’à aligner des siblings dans le même contexte.
3. Corrige donc le flux causal de la vue et limite `rank same` à des éléments frères, au lieu de bricoler le layout.
