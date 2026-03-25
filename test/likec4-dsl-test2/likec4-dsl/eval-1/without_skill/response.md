Minimal `projects/template/likec4.config.json` example:

{
  "name": "template",
  "include": {
    "paths": [
      "./**/*.c4",
      "../shared/**/*.c4"
    ]
  }
}

How project ownership works when multiple `likec4.config.json` files exist:
- Each `likec4.config.json` defines a separate LikeC4 project rooted at the folder that contains that config file.
- A `.c4` file is part of a project if that project discovers it through its own `include.paths` rules.
- Files inside `projects/template/` are naturally part of the `template` project when included from that config.
- Files in `projects/shared/` are not automatically attached to `template`; they become part of `template` only because `template` explicitly includes `../shared/**/*.c4`.
- If another project also includes the same shared files, those files are effectively reused by that project too. In other words, shared `.c4` files are selected per project config, not assigned once globally for the whole workspace.
