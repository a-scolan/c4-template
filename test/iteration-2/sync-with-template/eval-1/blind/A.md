Use a dedicated `sync/*` branch based on the upstream template, then bring over only the generic file.

1. Fetch the upstream template base.
   - `git fetch c4-template main`

2. Create a sync branch from `c4-template/main` — not from your current `main`.
   - `git switch -c sync/create-relationship-improvement c4-template/main`

3. Copy in only the generic file you want to propose upstream.
   - `git checkout main -- .github/skills/create-relationship/SKILL.md`

4. Review the exact diff before any push.
   - `git diff -- .github/skills/create-relationship/SKILL.md`
   - Confirm the change is generic, remove any project-specific examples or names, and do a confidentiality review.

5. Commit just that file.
   - `git add .github/skills/create-relationship/SKILL.md`
   - `git commit -m "sync: improve create-relationship guidance"`

6. Push the isolated `sync/*` branch.
   - `git push -u c4-template sync/create-relationship-improvement`

Do not push directly from `main`. If the diff fails the genericity or confidentiality review, discard the sync branch instead of pushing it.