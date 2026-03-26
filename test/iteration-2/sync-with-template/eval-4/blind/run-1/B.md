Good news: this is recoverable before PR.

### Goal
Keep only the generic skill change on `sync/spec-hardening` and remove local files.

```bash
# on sync/spec-hardening
git restore --source=c4-template/main -- projects/acme/system-model.c4 README.md

# if those files were committed in one or more commits, rewrite branch history:
git rebase -i c4-template/main
# drop or edit commits that touched local files

# verify branch now contains only upstream-safe assets
git diff --name-only c4-template/main...HEAD

# final confidentiality + genericity review
git show --name-only --stat
```

Expected final diff should include `.github/skills/create-element/SKILL.md` (and no `projects/acme/**`, no `README.md`).

If rebase is inconvenient, alternative fallback:
1. Create a fresh branch from `c4-template/main`.
2. Checkout only `.github/skills/create-element/SKILL.md` from your current branch.
3. Commit and open PR from the clean branch.