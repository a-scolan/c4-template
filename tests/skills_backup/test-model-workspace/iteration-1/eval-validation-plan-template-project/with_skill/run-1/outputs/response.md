Je ferais un pré-vol en 5 points :
1. `read-project-summary` pour confirmer que le kind du nouveau container existe dans les specs partagées et que tags/relations restent valides.
2. `search-element` pour vérifier que `mySystem.worker` existe bien avec le bon FQN partout où il est référencé.
3. `find-relationships` pour contrôler les types de relations et repérer un doublon ou une relation inversée.
4. Prévisualiser les vues touchées pour vérifier le rendu réel après l’ajout, puis relire les `include`.
5. Regarder le panneau Problems avant commit ; si la syntaxe est douteuse, vérifier la DSL LikeC4.
