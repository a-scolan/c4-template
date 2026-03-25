```likec4
model {
  api = service 'API' {
    #critical
    technology 'Node.js'
  }
}
```

It is invalid because inside an element body, tags must appear before properties. In the original snippet, `technology` (a property) comes before `#critical` (a tag), which violates LikeC4 ordering rules.