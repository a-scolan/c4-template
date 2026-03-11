Non : `projects/shared/` sert aux définitions réutilisables, pas des modèles projet-spécifiques.

Garde `paymentsCore` et `backOfficeUser` dans `projects/payments/`, sauf si tu crées un vrai externe partagé.

Pour les liens inter-projets, fais des références croisées explicites et minimales, par exemple via un projet `externals`.

Et évite les dépendances circulaires.