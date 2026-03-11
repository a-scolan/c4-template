Je partirais sur une structure simple : un environnement de prod, puis quelques zones, puis les VM qui hébergent les applications.

Concrètement, tu peux avoir une zone gateway, une zone services et une zone base de données, avec des serveurs dédiés pour le gateway, l'upload, le worker et MongoDB. Ensuite, ajoute les applications qui tournent sur chaque serveur.

Pour relier le déploiement au modèle logique, je ferais des liens vers les containers correspondants et je recréerais aussi les relations de déploiement importantes à la main pour que le diagramme reste lisible.

Pour la description, note surtout l'IP principale, le port et un résumé du rôle de chaque machine.