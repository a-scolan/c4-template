No. `projects/spec-showcase/container-views.c4` is not the authoritative taxonomy for another project.

Why not:
- it is a view file, so it filters kinds; it does not define them
- `README.md` explicitly says `projects/shared/` is the automation-facing source of truth, while `projects/spec-showcase/` is example material
- example content can drift or be selective; the actual kind declarations live in `projects/shared/spec-containers.c4`

Validate these first before adding a queue and API elsewhere:
1. the active target project's `likec4.config.json`
2. the exact shared kind names in `projects/shared/spec-containers.c4` (`Container_Api`, `Container_Queue`, and any supporting kinds)
3. the correct relationship types in `projects/shared/spec-global.c4` (`calls`, `async`, `reads`, `writes`)
4. the owning system and local model file structure in the target project
5. whether the target project already has naming/ID patterns you should follow

So: copy the idea of the view pattern if it helps, but validate taxonomy from `projects/shared/` and perform the actual queue/API modeling in the active target project's model files.
