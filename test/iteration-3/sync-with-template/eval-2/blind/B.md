Run targeted pulls only for the reusable workspace assets:

`git fetch c4-template main`
`git subtree pull --prefix=.github c4-template main --squash`
`git subtree pull --prefix=projects/shared c4-template main --squash`
`git push origin main`

Why `--squash`? It keeps the imported upstream history compact and easier to review, instead of dragging a long chain of upstream commits into your local history. The pull scope stays limited to `.github` and `projects/shared`; do not pull project-specific files such as `projects/<project>/`, ADRs, or `README.md` from the template upstream.
