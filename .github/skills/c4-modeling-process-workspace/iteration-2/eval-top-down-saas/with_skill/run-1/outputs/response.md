La bonne démarche LikeC4 pour partir de zéro sur un SaaS est :

1. **Si le workspace n’est pas clair, cadrer d’abord le projet** via `understand-project-structure`.
2. **C1** — définir la frontière du système, les acteurs et les externes.
3. **C2** — découper en containers runtime et documenter leurs relations.
4. **C3** — détailler seulement les containers complexes, risqués ou centraux.
5. **Dynamic / Use Cases** — **optionnel**, après C2, seulement si l’ordre temporel compte.
6. **Deployment** — **optionnel**, après structure stable, seulement si la topologie runtime compte.
7. **Validation** — finir par la vérification du modèle.

### Règle d’or

On conçoit **top-down C1 → C2 → C3**. On ne part ni des classes, ni des frameworks, ni de l’infra.
