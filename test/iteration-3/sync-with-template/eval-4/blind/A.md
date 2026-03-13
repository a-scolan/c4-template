Safest recovery: rebuild a clean upstream PR branch from `c4-template/main` and carry over only the generic skill change.

Commands:
1. `git fetch c4-template main`
2. `git branch backup/sync-spec-hardening`
3. `git switch -c sync/spec-hardening-clean c4-template/main`
4. `git checkout sync/spec-hardening -- .github/skills/create-element/SKILL.md`
5. `git diff -- .github/skills/create-element/SKILL.md`
6. `git add .github/skills/create-element/SKILL.md`
7. `git commit -m 'sync: harden create-element skill'`
8. `git show --name-only HEAD`
9. `git push c4-template HEAD:refs/heads/sync/spec-hardening-clean`

Then move the accidental local work to a separate local branch, for example:
- `git switch -c local/acme-followup backup/sync-spec-hardening`

If the mixed commit is only the latest local commit and you prefer to repair in place, an alternative is:
- `git reset --soft HEAD~1`
- `git restore --staged --worktree projects/acme/system-model.c4 README.md`
- `git commit -m 'sync: harden create-element skill'`

Do not open the PR to `c4-template` until `git show --name-only HEAD` lists only the generic `.github/skills/create-element/SKILL.md` change.
