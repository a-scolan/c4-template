---
name: sync-with-template
description: Use when pushing improvements to upstream template or pulling enhancements from other projects. Ensures generic content is separated from project-specific context.
---

# Sync with Template Upstream

## Overview

Manages bidirectional improvement flows between a derived project and its upstream template (c4-template) using git subtree. Generic content (skills, shared specs, copilot instructions) flows to the template; project-specific content stays local.

## Core Concept

A derived project contains two types of content:

| Content | Examples | Sync? | Why |
|---------|----------|-------|-----|
| **Generic** | `.github/skills/`, `projects/shared/spec-*.c4`, `.github/copilot-instructions.md` | ✅ YES | Reusable by all projects |
| **Project-Specific** | Project models, README.md, ADRs, documentation, configuration | ❌ NO | Unique to your project |

**Golden Rule:** Before pushing to template, remove ALL project-specific references and generalize.

---

## Quick Reference

### Always Push to Template ✅

```
.github/skills/**/*.md          # Skill improvements
.github/copilot-instructions.md # Workspace guidance
projects/shared/spec-*.c4       # Reusable specifications
projects/shared/images/         # Shared assets
```

### Never Push to Template ❌

```
projects/<your-project>/        # Project-specific models
README.md                        # Project introduction
ADR/                             # Project decisions
docs/                            # Project documentation
likec4.config.json              # Project configuration
```

---

## Workflow Summary

### Push Generic Improvements to Template

1. **Verify purity** - No project names or internal context
2. **Branch from template** - Create sync branch from c4-template/main
3. **Cherry-pick files** - Pull generic content from local main
4. **🔐 Confidentiality review** - Verify no secrets, internal architecture, or employee names
5. **Commit & push** - Clear message about improvements

**⚠️ CRITICAL:** If uncertain whether content is confidential (API details, internal architecture, security configs, employee names), **ask your team before pushing to public repository**. Leaked confidential info cannot be easily removed.

### Pull Improvements from Template

```bash
git fetch c4-template main
git subtree pull --prefix=.github c4-template main --squash
git subtree pull --prefix=projects/shared c4-template main --squash
git push origin main
```

---

## Complete Command Reference

See [WORKFLOW.md](WORKFLOW.md) for detailed step-by-step commands, troubleshooting, and real-world examples.

## Decision Tree: Is This Ready to Push?

```
Does it make sense for ANY project using c4-template?
  ├─ YES: Would another project need to adapt it? 
  │   ├─ NO → ✅ Can push (generic)
  │   └─ YES → ❌ Keep local (too specific)
  └─ NO: ❌ Keep local (project-specific)

Does it contain or mention:
  ├─ Project names → ❌ Remove before pushing
  ├─ Internal architecture → ❌ Generalize before pushing
  ├─ Credentials/security details → ❌ STOP and ask team
  ├─ Employee/team names → ❌ STOP and ask team
  └─ None of these → ✅ Safe to push
```

---

## 🔄 Complete Improvement Cycle

The template sync creates a continuous improvement loop:

```
1. Derived project improves a skill
   ↓
2. Abstract content (remove project-specific references)
   ↓
3. Create sync/... branch from c4-template/main
   ↓
4. Cherry-pick generic files
   ↓
5. Push to c4-template and create PR
   ↓
6. Reviewer approves PR on c4-template
   ↓
7. Merge into c4-template/main
   ↓
8. Other projects pull via subtree pull
   ↓
9. Derived project also pulls changes (+ improvements from other projects)
   ↓
10. Cycle continues...
```

---

## Best Practices

### ✅ Do

- ✅ Remove ALL project names before pushing to template
- ✅ Test generic files locally before pushing
- ✅ Write descriptive PRs explaining why the change matters
- ✅ Wait for approval before merging (if you have permissions)
- ✅ Use `--squash` for subtree pulls (clean history)
- ✅ Push from `sync/*` branches (never push main directly to template)
- ✅ Group changes logically (skills vs specs vs instructions)
- ✅ Verify purity before committing (Step 5 validation in WORKFLOW.md)

### ❌ Don't

- ❌ Mention the derived project in template skills
- ❌ Push project-specific files (ADRs, docs, README)
- ❌ Push confidential information (internal paths, API keys, security details)
- ❌ Force-push without reason (except rare emergencies)
- ❌ Leave `sync/*` branches long-lived (clean up after merge)
- ❌ Modify subtree files locally then pull (conflicts)
- ❌ Commit template changes mixed with project-specific changes
- ❌ Push to remote WITHOUT reviewing diffs first (risk of leaking secrets)

---

## Real-World Example: Improve and Push a Skill

**Scenario:** You fix a bug in `create-relationship/SKILL.md` and want to push it to template.

```bash
# 1. On main, make the fix
vim .github/skills/create-relationship/SKILL.md
git add .
git commit -m "fix: improve relationship syntax examples"

# 2. Verify no local context
grep -r "<foobar-project>\|your-project\|internal\|confidential" .github/skills/create-relationship/SKILL.md
# Should be empty

# 3. Create branch from template (use consistent naming)
git fetch c4-template main
git checkout -b sync/skills-template c4-template/main

# 4. Cherry-pick the change
git checkout main -- .github/skills/create-relationship/SKILL.md

# 5. Commit cleanly
git add .github/skills/create-relationship/SKILL.md
git commit -m "sync: improve relationship syntax examples

- Add clarity on calls vs async patterns
- Clarify when to use each kind
- Include real-world examples"

# 6. ⚠️ REVIEW BEFORE PUSHING
echo "Review changes:"
git diff --cached
echo ""
echo "🔐 CONFIDENTIALITY CHECK - Does this contain ANY:"
echo "  - Project-specific paths?"
echo "  - Internal API details?"
echo "  - Confidential architecture?"
echo "  - Security credentials?"
echo "  - Employee or team names?"
echo ""
echo "If UNCERTAIN or ANY yes: run 'git reset HEAD', clean up, and ask your team"
echo "If all no: proceed:"

# 7. Push and create PR
git push c4-template sync/skills-template --set-upstream
# Then create PR via GitHub UI
```

---

## Common Mistakes

- ❌ Pushing project-specific models, ADRs, or README content to the template
- ❌ Pushing directly from `main` — always use a `sync/*` branch
- ❌ Skipping the confidentiality review before pushing
- ❌ Committing project-specific and generic template changes in the same commit
- ❌ Omitting `--squash` on subtree pulls, polluting project commit history
- ❌ Leaving `sync/*` branches long-lived after the PR is merged

---

## Future: CI/CD Automated Sync

Future improvements could include GitHub Actions for:

1. **Quarterly Updates**: Auto-pull from c4-template and create PR
2. **Context Detection**: Scan files to push for local context leaks
3. **Validation**: Verify generic files load correctly in other projects

For now: execute manually following this skill's workflow.

---

## When in Doubt

**STOP and ask your team or manager:**
- Does this contain confidential information?
- Is this truly generic for all projects?
- Would another team benefit from this?

**Better safe than sorry** — confidential information in public repositories cannot be easily removed.
