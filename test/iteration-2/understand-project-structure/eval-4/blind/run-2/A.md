Great transition path from UML/ArchiMate to this LikeC4 workspace:

Start with local conventions first:

- C4 hierarchy discipline: C1 (actors/systems) → C2 (containers) → C3 (components)
- Concrete local kinds: `System_External`, `Container_Api`, `Container_Queue`, `Container_Database`, `Component`
- Deployment kinds are separate: `Node_Environment`, `Zone_*`, `Node_Vm`, `Node_App`
- Keep model relationships separate from deployment protocol relationships

Real sources of truth (in priority order):

1. Shared taxonomy: `projects/shared/spec-*.c4`
2. Cheat sheet: `projects/shared/SPEC_CHEATSHEET.md`
3. Active project summary/config (`likec4.config.json` wiring)

Important: `.github/skills/` is workflow guidance, not taxonomy authority. Example projects are learning references, not semantic truth.

Next handoff skill:

- Use `c4-modeling-process` if you are planning model sequence.
- Then use task-specific skills (`create-element`, `create-relationship`, `design-view`) once structure is validated.