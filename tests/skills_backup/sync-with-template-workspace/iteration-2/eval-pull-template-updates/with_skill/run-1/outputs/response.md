- `git fetch c4-template main`
- `git subtree pull --prefix=.github c4-template main --squash`
- `git subtree pull --prefix=projects/shared c4-template main --squash`

`--squash` garde un historique plus propre et plus compact.

Cette synchro vise `.github` et `projects/shared`, pas les fichiers projet-spécifiques.