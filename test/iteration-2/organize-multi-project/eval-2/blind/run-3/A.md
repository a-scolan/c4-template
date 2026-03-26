You should combine skills.

- Use **organize-multi-project** to design project boundaries and baseline structure.
- Use **configure-project-includes** to modify include paths and image aliases correctly.

Best sequence:
1. Create new project baseline files.
2. Update `include.paths` (relative paths only).
3. Normalize `imageAlias` entries to workspace convention.
4. Validate no circular dependency behavior and no absolute-path drift.

So this skill is necessary for structure, but include/image updates are better handled with the dedicated include-configuration skill.