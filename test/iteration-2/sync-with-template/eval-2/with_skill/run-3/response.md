Run:

```bash
git fetch c4-template main
git subtree pull --prefix=.github c4-template main --squash
git subtree pull --prefix=projects/shared c4-template main --squash
git push origin main
```

`--squash` keeps the sync concise by collapsing upstream subtree history into single integration commits, which improves readability, reviewability, and rollback handling.