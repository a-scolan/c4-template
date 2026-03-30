`#critical` is invalid in that position because a bare tag token is not a standalone field inside an element body. Tags must be declared through a tags field.

Minimal fix (keeping the same kind and both fields):

```likec4
model {
  api = service 'API' {
    technology 'Node.js'
    tags #critical
  }
}
```