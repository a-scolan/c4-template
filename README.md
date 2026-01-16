### Periodic Synchronization

Pull updates quarterly or when specifications change:

```bash
# Fetch latest
git fetch c4-template main

# Method 1: Git Subtree (integrates full directory trees)
git subtree pull --prefix=.github c4-template main --squash
git subtree pull --prefix=projects/shared c4-template main --squash
git subtree pull --prefix=projects/spec-showcase c4-template main --squash

# Method 2: Direct Checkout (targeted file updates - simpler for shared files)
git checkout c4-template/main -- .github/copilot-instructions.md .github/skills/
git checkout c4-template/main -- projects/shared/
git checkout c4-template/main -- projects/spec-showcase/

# Review and commit
git push
```

**What gets updated:**

| Path | Contains | Updates |
|---|---|---|
| `.github/copilot-instructions.md` | Copilot workflow guidance | When instructions change |
| `.github/skills/` | 14 Copilot agent skills | When skills are improved/added |
| `projects/shared/spec-*.c4` | Reusable specifications | When specs are updated |
| `projects/shared/images/` | Shared architecture icons | When new icons added |
| `projects/spec-showcase/` | Example diagrams | When examples improved |

**Note:** The `--squash` flag (with git subtree) consolidates all c4-template changes into a single commit per sync, keeping history clean. Updates are manual—subtrees do not auto-sync.

**Recommendation:** Use `git checkout` for targeted updates to `.github/` and `projects/shared/` since these are specifications and instructions that don't require full subtree history. Use `git subtree pull` if you want to preserve the full history of changes from the template.