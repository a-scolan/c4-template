Keep the edit surgical and make resolution order explicit.

For `include.paths`, do not replace the existing array. If the project already works with `../shared`, keep it and add `../platform-shared` as an additional relative source.

A safe default is:

```json
"include": {
  "paths": ["../shared", "../platform-shared"]
}
```

That keeps the current shared source first. If source resolution follows path order in your setup, keeping `../shared` first preserves existing behavior; only move `../platform-shared` earlier if you intentionally want it to override the earlier source.

For images, preserve the current shared alias if existing diagrams already rely on it:

```json
"imageAliases": {
  "@": "../shared/images/"
}
```

Do not blindly merge conflicting aliases under the same key. If `../platform-shared` introduces overlapping image alias names, use an explicit collision strategy such as:
- keep `@` for the current shared image base
- add a separate alias like `@platform` for platform-specific images
- or rename/prefix the conflicting aliases so it is obvious which source they come from

In short: append the new include, keep paths relative, preserve the stable shared alias, and resolve alias collisions with clear namespacing instead of implicit overrides.