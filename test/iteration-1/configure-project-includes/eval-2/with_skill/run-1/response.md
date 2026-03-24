Edit surgically:
- Append the new source to `include.paths`; do not replace existing entries.
- Keep all paths relative to the project folder.
- Preserve the working image alias, especially `"@": "../shared/images/"`, so current icons keep resolving.
- Avoid unrelated refactors or alias renames while changing includes.
- Do not switch to absolute paths.

In practice, turn `["../shared", "../platform-shared"]` into `["../shared", "../platform-shared", "../new-common-source"]` and leave the existing shared image alias intact unless you are deliberately migrating icon references.
