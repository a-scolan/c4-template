Smallest safe edit pattern:

1. In `include.paths`, append `"../platform-shared"` immediately after `"../shared"`.
2. Keep existing `imageAliases` entries untouched.
3. Add only new, namespaced aliases for platform images to avoid collisions.

Minimal JSON example:

{
  "include": {
    "paths": ["../shared", "../platform-shared"]
  },
  "imageAliases": {
    "shared_cloud": "../shared/images/cloud.svg",
    "platform_cloud": "../platform-shared/images/cloud.svg"
  }
}

If `shared_cloud` already exists, do not repoint it. Add `platform_cloud` (or similar) instead.Smallest safe JSON edit approach:

- Append `../platform-shared` after `../shared` in `include.paths`.
- Keep existing shared aliases unchanged.
- Add only new prefixed aliases for platform images.

Example minimal result in `projects/payments/likec4.config.json`:

{
  "include": {
    "paths": ["../shared", "../platform-shared"]
  },
  "imageAliases": {
    "shared.existing": "../shared/images/custom/existing.svg",
    "platform.newIcon": "../platform-shared/images/custom/new-icon.svg"
  }
}

If `platform-shared` has an image that matches an existing shared alias, do not overwrite `shared.existing`; add a new `platform.*` alias instead.