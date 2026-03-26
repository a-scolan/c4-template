Safe sequence (with confidentiality review) for remote `c4-template`:

```bash
git add .github/skills/create-relationship/SKILL.md
git commit -m "docs: improve create-relationship skill"

git fetch c4-template main
git checkout -b sync/skill-create-relationship c4-template/main

git checkout main -- .github/skills/create-relationship/SKILL.md
git add .github/skills/create-relationship/SKILL.md
git commit -m "docs: sync reusable skill update"

git show --name-only --stat
git push c4-template sync/skill-create-relationship --set-upstream
```

Before PR: verify no confidential or project-local context is present.