## Why the snippet is invalid

In LikeC4 DSL, **tags must come first inside an element body, before any properties**. The original snippet places `#critical` (a tag) after `technology 'Node.js'` (a property), which violates this ordering rule.

```likec4
model {
  api = service 'API' {
    technology 'Node.js'  // ← property
    #critical             // ← tag after property: INVALID
  }
}
```

## Corrected snippet

Move the tag before the property:

```likec4
model {
  api = service 'API' {
    #critical
    technology 'Node.js'
  }
}
```

Only the order was changed — the element kind (`service`), the tag (`#critical`), and the property (`technology`) are all preserved.
