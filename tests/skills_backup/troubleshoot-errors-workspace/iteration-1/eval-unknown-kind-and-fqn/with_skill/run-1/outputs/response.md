Ce sont deux causes différentes :
- `Container_WebUi` = kind inconnu : vérifie les kinds déclarés dans les specs partagées via `read-project-summary`, puis remplace-le par un kind existant.
- `api` = référence trop courte : dans ce projet le FQN attendu est probablement `mySystem.api`.

Commence donc par confirmer les kinds/tags/relations du projet, puis corrige les références. Évite de renommer au hasard : la cause racine est ici `kind invalide + FQN incomplet`.
