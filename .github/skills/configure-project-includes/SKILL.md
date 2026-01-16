---
name: configure-project-includes
description: Manage likec4.config.json includes and image aliases. Ensures relative paths and preserves existing configuration.
---

# Manage LikeC4 Project Includes

Use this skill when configuring project dependencies in likec4.config.json.

## Rules

1. **Relative paths:** Use `../shared` not absolute paths
2. **Preserve defaults:** Keep existing includes when adding new ones
3. **Image aliases:** Maintain `"@": "../shared/images"` for icon consistency
4. **Multiple specs:** Append to `paths` array, don't replace

## Example

```json
{
  "name": "my-project",
  "title": "My Project",
  "include": {
    "paths": ["../shared", "../common"]
  },
  "imageAliases": {
    "@": "../shared/images"
  }
}
```
