Once project context is established, the next skill should be **`c4-modeling-process`**.

## What this first skill must lock in before handoff

`understand-project-structure` should finish the workspace-framing work first:

- identify the active project in this multi-project repository
- confirm the project's `likec4.config.json` and includes
- anchor on the source of truth in `projects/shared/spec-*.c4`
- confirm the valid kinds, relationships, and tags actually available
- review the relevant model/view files for the chosen project
- use `read-project-summary` so the current project inventory is explicit rather than assumed

In this repository, that means grounding yourself in files such as:

- `projects/shared/spec-context.c4`
- `projects/shared/spec-containers.c4`
- `projects/shared/spec-components.c4`
- `projects/shared/spec-global.c4`
- the active project's `likec4.config.json`
- the active project's model and view files

## Why the handoff matters

- **`understand-project-structure`** is the framing skill: it tells you what workspace you are in, which taxonomy is legal, and which files are authoritative.
- **`c4-modeling-process`** is the sequencing skill: it decides the top-down modeling order, starting at **C1**, then **C2**, then selected **C3** only where justified.

So the handoff point is: once project, specs, kinds/relationships/tags, and relevant files are validated, switch to `c4-modeling-process` to orchestrate the actual modeling order. First frame the board, then play the game.