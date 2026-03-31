```likec4
model {
  api = service 'API' {
    #critical
    technology 'Node.js'
  }
}
```

This is invalid because `#critical` is a tag, and tags must appear before properties inside an element body. The original snippet placed the `technology` property first and the tag after it, which breaks the required body order.