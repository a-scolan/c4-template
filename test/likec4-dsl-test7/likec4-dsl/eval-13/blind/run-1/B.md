```likec4
model {
  api = service "API" {
    technology "Node.js"
    #critical
  }
}
```

The original snippet is invalid because LikeC4 string literals use double quotes, not single quotes. Only the title quoting was fixed; element kind (`service`), `technology`, and the `#critical` tag were kept unchanged.