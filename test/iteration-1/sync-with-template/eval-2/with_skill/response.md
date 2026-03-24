Run:
- `git fetch c4-template main`
- `git subtree pull --prefix=.github c4-template main --squash`
- `git subtree pull --prefix=projects/shared c4-template main --squash`
- `git push origin main`

Use `--squash` so each subtree update lands as a compact single change instead of importing the full upstream commit history into this derived repo. That keeps sync history readable, reduces noise, and makes it clear that you pulled shared workspace assets rather than mirroring the whole upstream graph.
