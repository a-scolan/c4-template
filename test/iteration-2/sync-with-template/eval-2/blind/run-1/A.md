To pull upstream improvements for `.github` and `projects/shared`:

1. Fetch upstream:
   - `git fetch c4-template`
2. Create/update a sync branch:
   - `git switch -c sync/upstream-dotgithub-shared c4-template/main`
3. Squash-merge upstream into your sync branch (single review commit):
   - `git merge --squash --no-commit c4-template/main`
4. Keep only target paths:
   - `git reset`
   - `git add .github projects/shared`
5. Commit the sync payload:
   - `git commit -m "sync: import upstream .github and projects/shared"`
6. Drop any unstaged leftovers from other paths:
   - `git restore --worktree --source=HEAD -- .`

Why `--squash`?
- Produces **one curated commit** for review instead of replaying many upstream commits.
- Makes cherry-picking to derived repos straightforward.
- Simplifies rollback (revert one commit).
- Keeps local history focused on “what was synced”, not upstream commit noise.