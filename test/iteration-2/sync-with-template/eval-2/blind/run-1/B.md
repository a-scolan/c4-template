To pull upstream improvements for `.github` and `projects/shared`, run:

```bash
git fetch c4-template main
git subtree pull --prefix=.github c4-template main --squash
git subtree pull --prefix=projects/shared c4-template main --squash
git push origin main
```

`--squash` is useful because it:
- keeps your local history compact (one merge commit per subtree update)
- avoids importing noisy upstream commit history into your repo
- makes review/revert simpler (one logical sync unit)

So you still receive upstream content changes, but with cleaner repository history in derived repos.