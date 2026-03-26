Use this skill plus another one.

- **organize-multi-project** gives structure decisions (project boundaries, baseline files, ownership).
- **configure-project-includes** is the companion for editing include paths and image aliases safely.

Recommended workflow:
1. Create project folder + minimum files.
2. Configure `include.paths` to shared content using relative paths.
3. Align `imageAlias` values with workspace standards.
4. Verify no absolute paths and no accidental dependency cycles.

So this skill is necessary, but for include/image changes it should be paired with `configure-project-includes`.