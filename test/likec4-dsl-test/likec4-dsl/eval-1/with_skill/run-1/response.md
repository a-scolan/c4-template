Minimal `projects/template/likec4.config.json`:

```json
{
  "$schema": "https://likec4.dev/schemas/config.json",
  "name": "template",
  "include": {
    "paths": ["../shared"]
  }
}
```

Project assignment rule: LikeC4 assigns each `.c4` file to the project whose config file is **nearest** in the directory hierarchy, walking upward from the file's location. When multiple config files exist in the workspace, the closest ancestor config wins — a file inside `projects/template/` belongs to `template`, not to any config sitting higher up. Files in `projects/shared/` have no config file of their own, so they are unowned by default; the `include.paths` directive explicitly pulls them into the `template` project regardless of their physical location.
