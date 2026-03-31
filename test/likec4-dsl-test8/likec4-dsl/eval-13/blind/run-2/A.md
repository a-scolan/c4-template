```likec4
model {
  api = service 'API' {
    #critical
    technology 'Node.js'
  }
}
```

It is invalid because in a LikeC4 element body, tags must come before properties. Here, `technology` is a property, so placing `#critical` after it breaks the required order.