1. `git fetch c4-template main`
2. `git checkout -b sync/update c4-template/main`
3. `git checkout main -- .github/skills/create-relationship/SKILL.md`
4. `git add .github/skills/create-relationship/SKILL.md && git commit -m "sync: improve create-relationship skill"`
5. `git diff --cached` puis revue confidentialité
6. `git push c4-template sync/update --set-upstream`

Et surtout : pas directement depuis `main`.