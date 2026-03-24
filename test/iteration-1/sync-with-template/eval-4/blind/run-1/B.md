Safest recovery: make a backup, rebuild the sync branch from upstream, and copy back only the generic file. Commands:
`git branch backup/sync-spec-hardening`
`git fetch c4-template`
`git switch -c sync/spec-hardening-clean c4-template/main`
`git restore --source=backup/sync-spec-hardening -- .github/skills/create-element/SKILL.md`
`git diff -- .github/skills/create-element/SKILL.md`
`git add .github/skills/create-element/SKILL.md`
`git commit -m "sync: harden create-element skill"`
`git push -u c4-template sync/spec-hardening-clean`
Leave `projects/acme/system-model.c4` and `README.md` on the backup/local branch; do not carry them into the upstream PR. If you must keep the original branch name, back it up first, then hard-reset `sync/spec-hardening` to `c4-template/main`, restore only the skill file from the backup branch, recommit, and force-push the cleaned branch.
