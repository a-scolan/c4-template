## What is invalid

`technology 'Node.js'` is missing the `=` assignment operator.

In LikeC4 DSL, body-level property declarations (like `technology`, `description`, `title`) use the form `keyword = 'value'`. Writing `technology 'Node.js'` without `=` is a syntax error because the parser expects an assignment, not a bare keyword followed by a string.

## Corrected snippet

```likec4
model {
  api = service 'API' {
    technology = 'Node.js'
    #critical
  }
}
```

Only `technology 'Node.js'` → `technology = 'Node.js'` was changed. Everything else (element kind `service`, tag `#critical`) is preserved as-is.
