## Why the snippet is invalid

Tags (`#critical`) **must come before any properties** inside an element body. In LikeC4 DSL, the required order is:

```
TAGS → PROPERTIES → nested elements / relationships
```

The original snippet places `technology 'Node.js'` (a property) before `#critical` (a tag), which violates this ordering rule.

## Corrected snippet

```likec4
model {
  api = service 'API' {
    #critical
    technology 'Node.js'
  }
}
```

The only change is moving `#critical` above `technology 'Node.js'`. No other modification is needed.
