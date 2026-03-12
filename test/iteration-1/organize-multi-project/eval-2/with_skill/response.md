Use this skill for the multi-project part: deciding where the new project lives, how to bootstrap it from the template, and how to keep project boundaries clean.

For the config details, combine it with `configure-project-includes`.

A practical split is:

- `organize-multi-project` → project layout, template-based bootstrap, shared-vs-project ownership
- `configure-project-includes` → `include.paths`, image aliases, and config consistency

Each project should still own its own `likec4.config.json`, and the shared specs should be referenced with a relative path such as `../shared`.

In this repo, the usual flow is:

1. Copy `projects/template/` into the new project folder.
2. Update that project’s `likec4.config.json`.
3. Keep `include.paths` relative to `../shared`.
4. Use `configure-project-includes` to verify or adjust the image alias and include settings.
