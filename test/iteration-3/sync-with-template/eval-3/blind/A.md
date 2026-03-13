Treat `projects/shared/spec-containers.c4` as a sync candidate, not an automatic sync.

Verify it is truly generic with this audit:
1. Ask whether another derived repository can use the fix without knowing your local domain.
2. Check whether it mentions project names, internal systems, customer details, private architecture, or one-off workarounds.
3. Confirm it is a reusable shared-spec improvement, not a repo-specific modeling tweak.
4. Run a confidentiality review on the exact diff before any push.

If it passes, use a safe upstream workflow:
- `git fetch c4-template main`
- `git switch -c sync/spec-containers-fix c4-template/main`
- `git checkout main -- projects/shared/spec-containers.c4`
- `git add projects/shared/spec-containers.c4`
- `git diff --cached`
- Re-check genericity/confidentiality, then commit and push the `sync/*` branch.

Rollback plan if it turns out too local or regressive:
- Before commit: `git restore --staged --worktree projects/shared/spec-containers.c4`
- Or delete the sync branch and recreate it from `c4-template/main`
- If the audit fails, keep the fix local and do not open the upstream PR.
