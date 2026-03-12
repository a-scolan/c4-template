Treat this as a targeted config edit, not a project reorganization.

Edit rules to follow:
- keep the existing `include.paths` entries
- append the new shared source instead of replacing the array
- keep paths relative to the project folder
- preserve the shared image alias so existing icons keep resolving

So if you currently have:

```json
"include": {
  "paths": ["../shared", "../platform-shared"]
}
```

add the new source like this:

```json
"include": {
  "paths": ["../shared", "../platform-shared", "../new-common-source"]
}
```

Also keep:

```json
"imageAliases": {
  "@": "../shared/images/"
}
```

Do not remove the existing alias, and do not switch to absolute paths. The safe pattern is: preserve what already works, add the new include surgically, and avoid unrelated config or file-structure changes.