Use a dedicated `sync/*` branch based on the template, then copy in only the generic file.

1. Fetch the template base.
   - `git fetch c4-template main`

2. Create a sync branch from the template base.
   - `git switch -c sync/create-relationship-improvement c4-template/main`

3. Bring over only the generic file from your current `main`.
   - `git checkout main -- .github/skills/create-relationship/SKILL.md`

4. Review before any push.
   - `git diff -- .github/skills/create-relationship/SKILL.md`
   - Confirm the file is still generic and remove any project-specific or confidential wording.

5. Commit the single-file change.
   - `git add .github/skills/create-relationship/SKILL.md`
   - `git commit -m "sync: improve create-relationship guidance"`

6. Push the `sync/*` branch.
   - `git push -u c4-template sync/create-relationship-improvement`

Do not push from `main`. If your improvement lives on another source branch, replace `main` in step 3 with that branch name, but still carry over only this one file.
