Your current `sync/spec-hardening` branch is polluted: `.github/skills/create-element/SKILL.md` is a possible upstream asset, but `projects/acme/system-model.c4` and `README.md` are local-only and must not be in the upstream PR.

Recover by rebuilding a clean sync branch from the upstream base and carrying forward only the generic file:
1. Keep the polluted branch only as a safety backup if needed.
2. Fetch the upstream base:
   `git fetch c4-template main`
3. Create a fresh clean branch from upstream, not from the polluted branch:
   `git switch -c sync/create-element-clean c4-template/main`
4. Bring over only the generic change:
   `git checkout sync/spec-hardening -- .github/skills/create-element/SKILL.md`
   `git add .github/skills/create-element/SKILL.md`
5. Review the staged diff and do the genericity/confidentiality check:
   `git diff --cached`
6. Commit and push the clean branch:
   `git commit -m "docs: improve create-element skill guidance"`
   `git push c4-template sync/create-element-clean --set-upstream`

Do not include `projects/acme/system-model.c4` or `README.md` in the upstream PR. If the cleanup shows the skill change itself is not truly generic, abort the sync by restoring the file or deleting the clean `sync/*` branch and keep the change local.
