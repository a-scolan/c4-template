Valide cette vue comme une vue C2 contextualisée, pas juste comme un extrait “propre” :
1. Vérifie que le parent explicite du contexte reste visible autour de `mySystem.webapp` et `mySystem.api`, sinon la vue perd son cadre.
2. Contrôle les `include` pour éviter un wildcard trop large qui ferait remonter des voisins non voulus.
3. Ouvre le rendu réel de la vue pour confirmer ce qui est effectivement inclus, pas seulement ce que le fichier laisse croire.
4. Pour les règles détaillées de contexte parent et de cadrage C2/C3, renvoie explicitement au skill `design-view`.
