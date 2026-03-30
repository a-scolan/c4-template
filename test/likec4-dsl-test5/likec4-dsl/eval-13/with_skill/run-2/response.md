```likec4
model {
  api = service 'API' {
    #critical
    technology 'Node.js'
  }
}
```

It is invalid because inside an element body, tags must come before properties; `technology` is a property, so `#critical` cannot appear after it.