---
name: understand-project-structure
description: Use when starting any LikeC4 modeling task, switching projects, or seeing unknown kind/relationship errors, to re-establish valid element kinds, relationship types, tags, and C1/C2/C3 structure before editing.
---

# Understand Project Structure

## Overview

Load project context before editing any model or view. This skill prevents invalid kinds, wrong relationships, and out-of-scope edits by validating project structure against shared specifications and current project summary.

## When to Use

- Start of any LikeC4 task (new conversation or new branch)
- Before creating/modifying elements, relationships, views, or deployment nodes
- After switching project in a multi-project workspace
- When errors mention unknown kinds/relationships or missing references

## C4 Framework Foundation

**REQUIRED BACKGROUND:** Read `c4-modeling-process` skill to understand the C4 methodology and design hierarchy (C1 Context → C2 Container → C3 Component).

## Workspace Structure

- **Shared specifications:** `projects/shared/spec-*.c4` - Source of truth for element kinds, relationship types, and tags
- **LikeC4 MCP (REQUIRED):** Required for project discovery and structure validation
- **Context7 MCP (AS NEEDED):** Use only when syntax/feature behavior is unclear
- **ADR documentation:** `ADR/` directory - System architecture decisions using standard ADR format

## Steps

1. **C4 Context (REQUIRED):** Read `c4-modeling-process` skill to understand design hierarchy
2. **Use LikeC4 MCP (REQUIRED):** Run `list-projects`, then `read-project-summary` for the active project
3. Read `likec4.config.json` to understand includes and image aliases
4. Check `projects/shared/spec-*.c4` for available element kinds, relationship types, and tags
5. Review existing model files to understand current C1/C2/C3 architecture
6. Resolve uncertainties with `read-element` / `search-element` before proposing changes
7. **Use Context7 MCP (optional):** Query LikeC4 documentation only for unresolved syntax/feature questions

## Quick Reference

| MCP Tool | When to use |
|----------|------------|
| `list-projects` | Find available projects in workspace |
| `read-project-summary` | Get all elements, kinds, tags for a project |
| `read-element` | Get details of a specific element |
| `search-element` | Find element by name, kind, or tag |

**Key files to read:**

```
likec4.config.json              # Includes and image aliases
projects/shared/spec-*.c4       # Element kinds, relationship types, tags
projects/<project>/system-model.c4  # Existing C1/C2/C3 model
```

## If Project Summary Looks Wrong

1. Re-run `list-projects` and confirm the intended project ID.
2. Re-run `read-project-summary` with the explicit project.
3. Verify `likec4.config.json` includes point to expected model files.
4. Verify shared specs are reachable and match expected kinds/relations.
5. If still inconsistent, stop edits and report the context as blocked/incomplete.

## Common Mistakes

- ❌ Skipping this skill and guessing element kind names
- ❌ Using `read-project-summary` only once — re-read after major model changes
- ❌ Ignoring `spec-*.c4` files in favor of guessing from other elements in the model
- ❌ Starting work without knowing which project is active in a multi-project workspace
- ❌ Treating Context7 as mandatory for every task (it is on-demand, not first step)

## Output

- Understanding of C4 framework and top-to-bottom design approach
- Complete understanding of project structure and architecture
- Available element kinds, relationship types, and tags
- Current C1/C2/C3 architecture organization
