---
name: understand-project-structure
description: Use when starting any LikeC4 modeling task, switching projects, or seeing unknown kind/relationship errors, to re-establish valid element kinds, relationship types, tags, and C1/C2/C3 structure before editing.
---

# Understand Project Structure

## Goal

Establish the workspace context **before** editing so you do not guess kinds, relationships, tags, or the active project.

This skill has two modes:

| Mode | What it optimizes for |
|---|---|
| **Preflight for editing** | Safe setup before changing elements, relationships, views, or deployment |
| **Onboarding for contributors** | Fast understanding of local conventions, sources of truth, and handoffs |

## When to Use

- Start of any LikeC4 task
- After switching project in a multi-project workspace
- Before C1/C2/C3/view/deployment edits
- When errors mention unknown kinds, relationships, or missing references
- When a contributor is new to this repository or to LikeC4

## Source-of-truth order

Always establish context in this order:

1. **Active project** — `list-projects`, then `read-project-summary` for the intended project
2. **Semantic taxonomy** — `projects/shared/SPEC_CHEATSHEET.md` and `projects/shared/spec-*.c4`
3. **Project wiring** — the project `likec4.config.json`, model files, and view files
4. **Workflow guidance** — `.github/skills/` tells you how to work, not what the taxonomy is

Important distinction:
- `projects/shared/spec-*.c4` = semantic source of truth
- `.github/skills/` = workflow guidance
- example projects such as `template` or `spec-showcase` = references only, **not** authoritative taxonomy

## Local conventions worth locking in early

Examples actually used here include:
- kinds such as `Container_Api`, `Container_Queue`, `Container_Database`, `System_External`, `Node_Vm`, `Node_App`
- model relationships such as `uses`, `calls`, `async`, `reads`, `writes`
- deployment relationship kinds such as `http`, `https`, `tcp`, `amqp`, `ldap`, `sql`, `redis`, `smtp`

Do not infer taxonomy from memory or from a nice-looking example file alone.

## Preflight for editing

Use this sequence before proposing changes:

1. confirm the active project
2. read the project summary
3. read shared specs and `SPEC_CHEATSHEET.md`
4. inspect the target project `likec4.config.json`
5. inspect the nearest model/view files that will actually be edited
6. only then hand off to the next editing skill

### MCP checks to re-run after switching projects

- `list-projects`
- `read-project-summary`
- `search-element` or `read-element` for the target boundary when needed

Re-run them after a project switch because stale context causes the exact failures this skill is meant to prevent: wrong project, wrong kind, wrong parent, wrong FQN.

## Onboarding for contributors

When the user is new to the repo, explain the workspace in this order:

1. where the shared taxonomy lives
2. where project-specific models and views live
3. which files are semantic truth vs workflow guidance
4. which next skill should take over once preflight is done

Good onboarding answers explicitly say that:
- `.github/skills/` helps with workflow, but does **not** override shared specs
- `projects/shared/spec-*.c4` and the project summary define valid kinds/relationships/tags
- example projects are there to learn patterns, not to redefine semantics

## Handoff after preflight

Once context is locked in, hand off deliberately:

- overall C1 → C2 → C3 sequencing → `c4-modeling-process`
- new element or property → `create-element`
- new relationship → `create-relationship`
- static/deployment view → `design-view`
- dynamic/use-case flow → `create-sequence-view`
- deployment structure → `model-deployment-infrastructure`

### Short handoff template

> Active project and shared taxonomy are validated. The next step is `<skill>` because the remaining task is `<modeling activity>`.

## If the project summary looks wrong

1. re-run `list-projects` and verify the intended project ID
2. re-run `read-project-summary` with the explicit project
3. verify the project `likec4.config.json` include paths
4. verify shared specs are reachable and match the expected kinds/relationships
5. if still inconsistent, stop and report the context as blocked instead of guessing

## If MCP is unavailable

Use an offline preflight instead of stalling:

1. read `projects/shared/SPEC_CHEATSHEET.md`
2. read `projects/shared/spec-*.c4`
3. read the target project `likec4.config.json`
4. read the nearby model/view files that will be edited
5. state what still needs MCP confirmation later (project summary, specific element lookup, relationship graph)

You should still be able to explain local conventions and safe next steps without MCP.

## Common mistakes

- ❌ guessing kinds from memory instead of revalidating the active project
- ❌ treating `.github/skills/` as the semantic source of truth
- ❌ using example projects as authoritative taxonomy
- ❌ editing C3 without checking the real parent container/system first
- ❌ assuming one `read-project-summary` run stays valid after switching projects or after major edits

## Output

Return a short preflight or onboarding guide that clearly states:
- active project or how to confirm it
- source-of-truth files
- valid local taxonomy examples
- risks avoided by the preflight
- the correct next skill to use
