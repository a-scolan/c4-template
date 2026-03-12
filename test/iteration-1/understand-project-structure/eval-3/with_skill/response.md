Once project context is established, the next skill should be **`c4-modeling-process`**.

## What this first skill must lock in before handoff

Before handoff, `understand-project-structure` should establish all of the workspace framing information that the sequencing skill depends on:

1. **Active project**
   - Confirm which project is being edited.
   - In this repository, visible project ids include `template-project` and `spec-showcase`.

2. **Project-level source of truth**
   - Read the active `likec4.config.json`.
   - Confirm includes and image aliases so you know which shared specs are actually in play.

3. **Valid local taxonomy**
   - Kinds from shared specs: context kinds, container kinds, component kinds, and deployment kinds.
   - Relationship types from shared specs: model relationships and deployment relationships.
   - Tags from shared specs: global tags, container tags, deployment tags.

4. **Relevant files to edit or inspect next**
   - Shared specs under `projects/shared/`
   - The active project model files
   - The active project view files
   - Any existing view organization such as `C1`, `C2`, `C3`, `Use Cases`, or `Deployment`

5. **Current architecture shape**
   - What already exists at C1
   - What already exists at C2
   - Whether C3 already exists, and for which containers

6. **Open uncertainties**
   - Any unclear parent container, missing reference, or suspected taxonomy mismatch should be resolved before handoff.

## Why the handoff matters

- **`understand-project-structure`** is the workspace-framing skill. Its job is to prevent invalid edits by grounding the work in the active project, shared specs, valid kinds/relationships/tags, and current file structure.
- **`c4-modeling-process`** is the sequencing skill. Its job is to decide the correct top-down modeling order: **C1 → C2 → selective C3**, and then hand off the detailed edit to skills such as `create-element`, `create-relationship`, or `design-view`.

## Handoff point

Hand off to `c4-modeling-process` only after project, taxonomy, relevant files, and current structure are locked in. That way the next skill can focus on modeling order instead of re-discovering workspace rules.