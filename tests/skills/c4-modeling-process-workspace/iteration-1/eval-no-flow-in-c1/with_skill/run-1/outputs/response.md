Non.

Un **C1** doit rester **statique** : il montre le **contexte**, la **frontière du système**, les **acteurs** et les **systèmes externes**.  
Il ne doit pas montrer un **enchaînement temporel**.

Dans ton cas :

- **`webapp`** et **`API`** sont des **containers** → ça relève du **C2**, pas du C1.
- Le **parcours utilisateur avec ordre des étapes** (“user puis webapp puis API”) doit aller dans **`views 'Use Cases'`** sous forme de **`dynamic view`**.

En bref :

- **C1** = qui entoure le système
- **C2** = webapp, API, DB, etc.
- **Use Cases / dynamic view** = **ordre temporel** des interactions

Donc si tu veux montrer **le scénario**, mets-le en **vue dynamique**.  
Si tu veux seulement montrer que **user utilise la webapp** et que **la webapp appelle l’API** sans notion de temps, fais plutôt une **vue C2 statique**.
