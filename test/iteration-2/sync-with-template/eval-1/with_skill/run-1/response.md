Use this safe workflow to push the skill improvement to `c4-template` via a `sync/*` branch:

```bash
git add .github/skills/create-relationship/SKILL.md
git commit -m "docs(skill): improve create-relationship guidance"

git fetch c4-template main
git checkout -b sync/skill-create-relationship c4-template/main

git checkout main -- .github/skills/create-relationship/SKILL.md

git add .github/skills/create-relationship/SKILL.md
git commit -m "docs(skill): sync create-relationship improvements"

git show --name-only --stat

git push c4-template sync/skill-create-relationship --set-upstream
```

Before opening the PR, run a **confidentiality review** on the file content and diff:
- no project-local paths
- no internal/private architecture details
- no credentials/secrets
- no employee/customer identifiers

If anything local slipped in, remove it from the branch before PR.