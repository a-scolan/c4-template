Je diagnostiquerais ça par cause racine :
1. `read-project-summary` pour lister les kinds réellement valides dans le projet et confirmer que `Container_WebUi` n’existe pas dans les specs partagées.
2. Corriger ensuite le kind vers un kind réellement défini, au lieu de renommer au hasard.
3. Pour `Element not found: api`, partir de l’hypothèse qu’il manque le FQN complet : `mySystem.api` plutôt que `api`.
4. Rechercher enfin les références courtes restantes et revalider après correction.
