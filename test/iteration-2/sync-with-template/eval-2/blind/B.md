To pull only the shared workspace assets from the upstream reference repo, run:

- `git fetch c4-template main`
- `git subtree pull --prefix=.github c4-template main --squash`
- `git subtree pull --prefix=projects/shared c4-template main --squash`
- `git push origin main`

Why these commands:
- `.github` and `projects/shared` are the reusable sync surfaces for workspace-level assets.
- They avoid pulling project-specific content such as `projects/<project>/`, ADRs, or local docs.

Why `--squash`:
- it keeps the history compact
- it avoids importing a long stream of upstream commits into your local history
- it makes the sync easier to review as a single consolidated change

So the idea is: fetch once, pull only the shared asset trees, keep history clean with `--squash`, and do **not** subtree-pull project-local files.