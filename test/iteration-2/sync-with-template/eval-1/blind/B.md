Use a dedicated `sync/*` branch based on the upstream template, and bring over only the generic file.

1. Make sure your local improvement exists on your current `main` branch.
2. Fetch the upstream reference branch:
   - `git fetch c4-template main`
3. Create a dedicated sync branch from the upstream base:
   - `git checkout -b sync/create-relationship-skill c4-template/main`
4. Bring over only the reusable file from your local `main` branch:
   - `git checkout main -- .github/skills/create-relationship/SKILL.md`
5. Stage it:
   - `git add .github/skills/create-relationship/SKILL.md`
6. Review the staged diff and do the confidentiality check **before** pushing:
   - `git diff --cached`

Confidentiality/genericity review before push:
- remove project-specific paths
- remove internal API or architecture details
- remove team or employee names
- confirm the wording is reusable across derived repositories

7. Commit only that generic change:
   - `git commit -m "docs: improve create-relationship skill"`
8. Push the sync branch to the upstream remote:
   - `git push c4-template sync/create-relationship-skill --set-upstream`

Key safety rules:
- branch from `c4-template/main`, not from your local `main`
- bring over only `.github/skills/create-relationship/SKILL.md`
- do the diff/confidentiality review before `git push`
- never push directly from `main`