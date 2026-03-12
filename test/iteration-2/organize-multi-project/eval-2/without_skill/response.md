For the **multi-project structure and bootstrap**, this guidance is enough.

For the exact configuration details—especially `include.paths` and `imageAliases`—treat that as a **separate config-focused step**.

The important structural rules are:

- each project has its **own** `likec4.config.json`
- each project stays self-contained with a small split such as `system-model.c4` + `system-views.c4`
- shared specs and shared images stay under `projects/shared/`

For the config itself, keep using relative paths back to shared assets, typically:

- `include.paths: ["../shared"]`
- image aliases pointing to `../shared/images/`

So: use this guidance to decide **where the new project lives and what files it owns**, then handle the include/image wiring as its own configuration task inside that project's `likec4.config.json`.
