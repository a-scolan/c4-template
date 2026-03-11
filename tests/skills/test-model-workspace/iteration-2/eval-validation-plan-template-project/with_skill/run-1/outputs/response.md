Je ferais la validation en 5 contrôles, dans cet ordre :
1. `read-project-summary` pour confirmer que le kind utilisé par `mySystem.worker`, les tags et les relations attendues existent bien dans les specs partagées.
2. `search-element` pour vérifier que `mySystem.worker` est bien résolu partout avec le bon FQN, sans référence courte ambiguë.
3. `find-relationships` pour contrôler les types de relations ajoutées, repérer un doublon et vérifier qu’on n’a pas inversé un flux.
4. Prévisualiser les vues touchées pour vérifier le rendu réel de la nouvelle vue C2 et relire les `include` / le contexte.
5. Finir par le panneau Problems avant commit ; si la syntaxe est douteuse, confirmer la DSL LikeC4 avant de pousser.
