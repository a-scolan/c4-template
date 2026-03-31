```likec4
model {
  api = service 'API' {
    #critical
    technology 'Node.js'
  }
}
```

This snippet was invalid because in a LikeC4 element body, tags must come before properties. Here, `technology 'Node.js'` starts the properties section, so placing `#critical` after it breaks the element-body order.

The minimal fix is to move `#critical` above `technology` and leave everything else unchanged.
