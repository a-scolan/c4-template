```likec4
model {
  api = service 'API' {
    #critical
    technology 'Node.js'
  }
}
```

It is invalid because, inside an element body, tags must appear before properties. Here `#critical` was placed after the `technology` property.