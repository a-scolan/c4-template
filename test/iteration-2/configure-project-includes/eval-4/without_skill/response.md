Preserve current behavior first, then add the new source deliberately.

Recommended shape:

```json
{
  "include": {
    "paths": [
      "../shared",
      "../platform-shared"
    ]
  },
  "imageAliases": {
    "@": "../shared/images/",
    "@platform": "../platform-shared/images/"
  }
}
```

Rules to follow:

- Add `../platform-shared`; do not replace `../shared`.
- Keep paths relative to `projects/payments/`.
- `include.paths` order matters for resolution. If current references must keep resolving from `../shared`, leave `../shared` first and add `../platform-shared` after it.
- Do not blindly merge colliding image aliases.
- Keep the existing `@` alias stable if diagrams already depend on it.
- Give the new source its own explicit alias or prefix, such as `@platform`, or rename conflicting aliases clearly.
- Only reverse the include order if you intentionally want `../platform-shared` to override existing definitions, and then verify the affected imports.