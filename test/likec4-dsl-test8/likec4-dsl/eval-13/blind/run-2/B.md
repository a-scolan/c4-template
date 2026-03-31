```likec4
model {
  api = service 'API' #critical {
    technology 'Node.js'
  }
}
```

Why it was invalid:
- `#critical` is inline tag syntax.
- In LikeC4, inline tags belong on the element declaration line, not as a standalone statement inside the element body.
- `technology 'Node.js'` is already valid, so the only necessary fix is moving the tag.