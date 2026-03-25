```likec4
model {
  api = service 'API' {
    #critical
    technology 'Node.js'
  }
}
```

The original snippet is invalid because in an element body, tags must appear before properties. Here, `technology 'Node.js'` (a property) was placed before `#critical` (a tag), which violates LikeC4 ordering rules.