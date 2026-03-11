Non. Une vue **C3 n’est pas obligatoire** pour chaque container.

La règle de décision est simple :

- on modélise d’abord **C1**, puis **C2**
- on ne fait une **C3** que si le container **“le mérite”**
- il le mérite s’il est :
  - **central** dans l’architecture
  - **risqué** ou difficile à raisonner
  - **assez complexe en interne** pour que la vue C2 ne suffise plus

Donc, pour un **petit container API très simple**, la réponse est généralement **non** : si la **C2 explique déjà bien** son rôle et ses interactions, **on s’arrête à C2**.

En une phrase : **C3 est optionnelle et sélective, pas systématique**.
