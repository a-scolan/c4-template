# Sync with Template: Simple Commands

⚠️ **CRITICAL SAFETY RULES BEFORE EVERY PUSH:**
1. **NO project names** (capsule, lemonldap-ng, etc.)
2. **NO internal paths** (C:/, /home/, project folders)
3. **NO secrets** (API keys, tokens, passwords)
4. **NO internal architecture** or employee names
5. **ALWAYS review diffs** before pushing

**If ANY DOUBT: STOP and ask your team.**

---

## Push One Skill to Template

```bash
# 1. Get template main
git fetch c4-template main
git checkout -b sync/update c4-template/main

# 2. Add your improved skill (one at a time)
git checkout main -- .github/skills/create-element/SKILL.md

# 3. Check what changed
git diff --cached | head -100
# Any project names? Internal paths? Secrets?
# If YES → git reset HEAD, fix, try again
# If NO → continue

# 4. Commit
git commit -m "sync: improve create-element skill

- Better examples
- Clearer guidance"

# 5. Push
git push c4-template sync/update --set-upstream
```

---

## Pull Updated Skills from Template

```bash
git fetch c4-template main
git subtree pull --prefix=.github c4-template main --squash
git subtree pull --prefix=projects/shared c4-template main --squash
git push origin main
```

---

## If Merge Conflicts

```bash
# Edit conflicted files
git add .
git commit -m "resolve: merge template updates"
git push origin main
```

---

## Remember

- Push from `sync/update` branch (never main)
- Review diffs before every push
- One skill at a time (safer)
- Ask your team if unsure

**See SKILL.md for concepts and best practices.**
