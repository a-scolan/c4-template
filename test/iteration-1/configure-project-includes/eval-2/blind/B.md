Treat this as a targeted config edit.

Edit `include.paths` by adding the new shared source without replacing the existing entries. If you already have:

- `../shared`
- `../platform-shared`

keep both, then append the new source in the position you want.

Rules to follow:

- preserve every existing include path unless you intentionally want different resolution behavior
- add the new path without overwriting the array
- keep paths relative to the project folder
- avoid absolute paths

For icons, keep the existing shared image alias in place rather than removing or repointing it. If you need images from the new shared source too, add a separate alias instead of replacing the current one.

In short: extend the config, do not rewrite it; preserve the current include paths and keep the shared image alias working as-is.