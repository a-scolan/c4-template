The corrected minimal snippet is:

```likec4
model {
  api = service 'API' #critical {
    technology 'Node.js'
  }
}
```

Why the original is invalid:

- `#critical` uses LikeC4 tag syntax.
- In this syntax, a `#tag` is attached to the element declaration itself.
- It is **not** a standalone statement inside the element body.
- `technology 'Node.js'` is fine as written, so the only necessary fix is to move the tag onto the declaration line for `api`.
