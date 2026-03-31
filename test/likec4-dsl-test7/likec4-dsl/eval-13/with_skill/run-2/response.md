```likec4
model {
  api = service 'API' {
    #critical
    technology 'Node.js'
  }
}
```

It is invalid because inside an element body, tags must come before properties. Here, `technology` is a property and `#critical` is a tag, so the tag has to be moved above the property.