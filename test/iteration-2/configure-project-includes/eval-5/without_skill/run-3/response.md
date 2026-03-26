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

If `shared_cloud` already exists, do not repoint it. Add `platform_cloud` (or similar) instead.