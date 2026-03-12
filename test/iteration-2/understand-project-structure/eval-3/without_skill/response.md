Once the project context is established, the next step should hand off to **`c4-modeling-process`** to drive the actual **C1 → C2 → C3** modeling sequence.

## What the initial framing pass must lock in before that handoff
- **Active project**: which project folder you are modeling in
- **Source-of-truth files**:
  - the project's `likec4.config.json`
  - the shared specs under `projects/shared/`
  - the project-local model/view files
  - the project summary, if available, as the assembled context check
- **Valid taxonomy** for the selected project:
  - allowed kinds
  - allowed relationships
  - relevant tags
- **Target modeling scope**:
  - which system is the C1 anchor
  - which containers belong in C2
  - whether a C3 breakdown is needed yet, and for which container
- **Naming and structural rules** already used in this repository, such as exact names like `Container_Api` and the existing C1/C2/C3 layering

## Role split
- **Initial framing pass:** establish workspace context, confirm the real sources of truth, and prevent wrong-project or wrong-taxonomy edits
- **`c4-modeling-process`:** sequence the actual modeling work in order, from context to containers to components

So the handoff point is: **after project, taxonomy, tags, and relevant files are locked in; before any new C1/C2/C3 content is authored**.
