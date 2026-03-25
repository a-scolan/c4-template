```likec4
model {
  api = component 'API' {
    technology 'Node.js'
    #critical
  }
}
```

It is invalid because `service` is not a valid built-in element kind in LikeC4 unless it is declared in `specification` first. Replacing it with a valid kind (`component`) is the minimal fix.