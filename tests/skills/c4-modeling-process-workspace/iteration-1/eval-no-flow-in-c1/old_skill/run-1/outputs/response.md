Non.

Un **C1 doit rester statique** : il montre la **frontière du système** et **qui/quoi interagit** avec lui.  
Des **flèches temporelles** pour un parcours utilisateur relèvent d’un **workflow runtime**, pas d’un contexte.

Dans ton cas :

- **`user -> système`** : oui, c’est du **C1**
- **`user -> webapp -> API` avec ordre temporel** : non, ce n’est **pas** du C1

Ce diagramme doit aller dans **`views 'Use Cases'`** sous forme de **vue dynamique**.

Pourquoi :
- **C1** répond à : *« qui interagit avec le système ? »*
- **vue dynamique / Use Cases** répond à : *« comment le scénario se déroule dans le temps ? »*

Et détail important : **webapp** et **API** sont en général des **containers**, donc déjà plutôt du **C2**.  
Donc :
- si tu veux montrer **webapp + API** sans temporalité → **C2**
- si tu veux montrer leur **enchaînement dans un scénario utilisateur** → **Dynamic view dans `Use Cases`**
