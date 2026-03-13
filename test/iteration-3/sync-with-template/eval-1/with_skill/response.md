Use a narrow `sync/*` flow that carries only the generic file:

1. Make sure the improvement exists locally on `main`.
2. Fetch the upstream base and create a dedicated sync branch from it:
   `git fetch c4-template main`
   `git switch -c sync/create-relationship-skill c4-template/main`
3. Bring over only the generic file from your local branch:
   `git checkout main -- .github/skills/create-relationship/SKILL.md`
   `git add .github/skills/create-relationship/SKILL.md`
4. Review before any push:
   `git diff --cached`
   Then do the confidentiality/genericity review: confirm the skill text is reusable, and remove any local project names, private architecture details, team/customer references, or secrets.
5. Commit the isolated change:
   `git commit -m "docs: improve create-relationship skill guidance"`
6. Push the sync branch, not `main`:
   `git push c4-template sync/create-relationship-skill --set-upstream`

That keeps the workflow scoped to one generic improvement and avoids broad repo synchronization.
