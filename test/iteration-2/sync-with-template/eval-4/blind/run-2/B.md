Recovery approach before PR:

```bash
# stay on sync/spec-hardening
git restore --source=c4-template/main -- projects/acme/system-model.c4 README.md

# clean prior commits if they already captured local files
git rebase -i c4-template/main

# verify only upstream-safe assets remain
git diff --name-only c4-template/main...HEAD
git show --name-only --stat
```

Desired final state: branch contains only `.github/skills/create-element/SKILL.md` (no `projects/acme/**`, no `README.md`).

Alternative: create a fresh `sync/*` branch from `c4-template/main`, cherry-pick or checkout only the good skill file, recommit, open PR.