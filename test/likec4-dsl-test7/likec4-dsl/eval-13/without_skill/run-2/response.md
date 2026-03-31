```likec4
model {
  api = service 'API' {
    technology 'Node.js'
    tags #critical
  }
}
```

`#critical` alone is invalid in this position because tags must be declared with the `tags` keyword. The snippet keeps the same element kind (`service`) and preserves both required fields (`technology` and the `critical` tag), changing only what is necessary.