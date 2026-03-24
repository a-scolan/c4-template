Safe sequence:
1. Commit the local fix on your normal local branch:
   - `git add .github/skills/create-relationship/SKILL.md`
   - `git commit -m 'fix: improve create-relationship skill guidance'`
2. Branch from the upstream reference repo, not from `main`:
   - `git fetch c4-template main`
   - `git checkout -b sync/create-relationship-skill c4-template/main`
3. Bring over only the generic file:
   - `git checkout main -- .github/skills/create-relationship/SKILL.md`
4. Review the staged diff and do the confidentiality review before creating the sync commit:
   - `git diff --cached`
   - Verify the file does **not** contain project-specific paths, internal API details, confidential architecture notes, security credentials, or employee/team names.
5. Commit only that generic change on the sync branch:
   - `git commit -m 'sync: update create-relationship skill'`
6. Push the sync branch and open a PR to the upstream repo:
   - `git push c4-template sync/create-relationship-skill --set-upstream`

Do not push directly from `main`. If the audit fails, keep the change local or remove it from the sync branch before pushing.
