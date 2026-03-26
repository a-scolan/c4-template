Safe push sequence with `sync/*` branch and confidentiality gate:

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

Confidentiality review before PR: remove any internal system names, customer info, secrets, private architecture notes, or team/person identifiers.