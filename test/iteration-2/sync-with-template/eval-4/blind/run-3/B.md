Recover by removing local files from the sync branch before PR:

```bash
# on sync/spec-hardening
git restore --source=c4-template/main -- projects/acme/system-model.c4 README.md

# if already committed, rewrite commits touching local files
git rebase -i c4-template/main

# verify final branch content
git diff --name-only c4-template/main...HEAD
git show --name-only --stat
```

Target result: only generic upstream-safe change remains (`.github/skills/create-element/SKILL.md`).

Fallback: create a fresh branch from `c4-template/main`, bring only the good skill file, commit, PR.