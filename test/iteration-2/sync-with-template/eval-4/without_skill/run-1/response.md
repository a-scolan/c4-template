Recover by rebuilding a clean branch that keeps only the generic skill change.

1. Safety backup:
   - `git switch sync/spec-hardening`
   - `git branch backup/sync-spec-hardening`

2. Identify mixed commit(s):
   - `git log --oneline c4-template/main..HEAD`

3. Create clean branch from upstream base:
   - `git switch -c sync/spec-hardening-clean c4-template/main`

4. Reapply only intended change:
   - `git cherry-pick -n <mixed_commit_sha>`
   - Remove accidental files from index + worktree:
     - `git restore --staged --worktree projects/acme/system-model.c4 README.md`

5. Commit clean payload:
   - `git commit -m "sync: harden create-element skill guidance"`

6. Verify branch purity:
   - `git diff --name-only c4-template/main...HEAD`
   - Must show only `.github/skills/create-element/SKILL.md`.

7. Push and open PR:
   - `git push -u c4-template sync/spec-hardening-clean`

This avoids risky history surgery on the original branch and guarantees a PR with only upstream-safe changes.