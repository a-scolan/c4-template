Commands to pull upstream shared assets:

```bash
git fetch c4-template main
git subtree pull --prefix=.github c4-template main --squash
git subtree pull --prefix=projects/shared c4-template main --squash
git push origin main
```

Why `--squash`:
- keeps sync history compact and readable
- avoids importing full upstream commit graph
- makes audits and rollback easier (single logical sync commit per pull)