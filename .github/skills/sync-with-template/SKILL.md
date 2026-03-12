---
name: sync-with-template
description: Use when deciding whether shared skills, shared specs, workspace instructions, or other reusable assets should be pulled from or pushed to an upstream reference repository, especially when you need to separate generic changes from project-local content.
---

# Sync Generic Workspace Assets with Upstream

## Overview

This skill manages synchronization between the **current repository** and an **upstream reference repository** for reusable workspace assets such as `.github/` and `projects/shared/`.

It is **not** about the example model under `projects/template/`. It is about deciding what parts of the current repo are generic enough to travel upstream or safe enough to pull back down.

## When to Use

- Reviewing a mixed diff to decide what is syncable upstream vs local-only
- Pushing generic improvements in skills, shared specs, or shared instructions
- Pulling upstream updates for `.github` or `projects/shared`
- Running a genericity/confidentiality review before push

**Do not use** for editing project models, ADR content, or deciding how the example project itself should be modeled.

## Core Concept

Separate the repo into two buckets:

| Content | Examples | Sync upstream? | Why |
|---------|----------|----------------|-----|
| **Reusable workspace assets** | `.github/skills/`, `.github/copilot-instructions.md`, `projects/shared/spec-*.c4`, `projects/shared/images/` | ✅ Yes | Helpful across multiple derived repositories |
| **Project-local content** | `projects/<project>/`, `README.md`, `ADR/`, `docs/`, project `likec4.config.json` | ❌ No | Tied to one repository, one domain, or one team |

**Golden Rule:** Before pushing upstream, remove project-local context and verify the change is reusable outside the current repository.

## Quick Reference

### Usually Sync Upstream ✅

```
.github/skills/**/*.md
.github/copilot-instructions.md
projects/shared/spec-*.c4
projects/shared/images/
```

### Usually Keep Local ❌

```
projects/<your-project>/
README.md
ADR/
docs/
likec4.config.json
```

### Upstream Remote

Use your workspace's upstream remote and default branch.
In this repository, that upstream is often `c4-template/main`.

## Push Workflow

1. **Audit genericity** — confirm the change benefits multiple repositories.
2. **Audit confidentiality** — remove secrets, internal architecture, employee names, and private context.
3. **Branch from upstream** — create a dedicated `sync/*` branch from the upstream default branch.
4. **Bring over only generic files** — cherry-pick or checkout just the reusable assets.
5. **Review the diff** — verify the branch contains only intended upstream content.
6. **Push and open a PR** — never push straight from `main`.

If the audit fails, keep the change local. If you already started the sync branch, drop the file from the branch or reset the branch before pushing.

## Pull Workflow

Pull only the reusable workspace assets you actually consume.

```bash
git fetch c4-template main
git subtree pull --prefix=.github c4-template main --squash
git subtree pull --prefix=projects/shared c4-template main --squash
git push origin main
```

If your upstream remote or branch name differs, substitute it consistently.

## Decision Test

Ask these questions in order:

1. **Would another derived repository use this without knowing our local domain?**
2. **Does it mention project names, internal systems, customer details, or private architecture?**
3. **Is it workspace-level (`.github`, `projects/shared`) rather than project-local (`projects/<project>`, ADRs, docs)?**
4. **Can I explain the change as a reusable improvement rather than a one-off workaround?**

If any answer points to local context, keep the change in the current repo.

## Example: Push One Generic Skill Fix Upstream

```bash
# 1. Commit the local fix on main
git add .github/skills/create-relationship/SKILL.md
git commit -m "fix: clarify relationship examples"

# 2. Branch from the upstream reference repository
git fetch c4-template main
git checkout -b sync/skills-template c4-template/main

# 3. Bring only the generic file onto the sync branch
git checkout main -- .github/skills/create-relationship/SKILL.md

# 4. Review before pushing
git diff --cached

# 5. Push the sync branch
git push c4-template sync/skills-template --set-upstream
```

Before step 5, verify the file does **not** contain:
- project-specific paths
- internal API details
- confidential architecture notes
- security credentials
- employee or team names

## Best Practices

### ✅ Do

- ✅ Treat `.github` and `projects/shared` as the main upstream sync surfaces
- ✅ Use `sync/*` branches for upstream pushes
- ✅ Review diffs before every push
- ✅ Use `--squash` for subtree pulls to keep history compact
- ✅ Keep generic and project-local changes in separate commits when possible
- ✅ Ask for review if the genericity of a change is debatable

### ❌ Don’t

- ❌ Confuse upstream sync with the contents of `projects/template/`
- ❌ Push project models, ADRs, README content, or local docs upstream
- ❌ Skip the confidentiality review
- ❌ Push directly from `main`
- ❌ Mix upstream-bound changes and local-only changes in the same sync branch
- ❌ Leave `sync/*` branches long-lived after merge

## Common Mistakes

❌ **Treating the example project as the sync target** — this skill is about workspace asset sync, not about changing `projects/template/`

❌ **Assuming every change under `projects/shared` is automatically generic** — some fixes still encode local assumptions and must be reviewed

❌ **Skipping rollback thinking** — if a sync branch starts to include local context, remove the file from the branch or reset the branch before pushing

❌ **Pulling project-local files with subtree** — only pull shared workspace assets from upstream

## When in Doubt

Pause and ask:
- Is this reusable outside the current repository?
- Would I be comfortable showing this diff to another team?
- Does this belong in `.github` or `projects/shared`, or is it really project-local?

Better to keep a change local than to publish local context upstream by mistake.
