The snippet is invalid because tags must come before properties inside an element body.

```likec4
model {
  api = service 'API' {
    #critical
    technology 'Node.js'
  }
}
```