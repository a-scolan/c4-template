```likec4
model {
  extend cloud.api {
    metadata {
      port "9090"
      region "us-east-1"
    }
    health = component "Health Check"
  }
}
```

`port` becomes `["8080", "9090"]` in the merged model. It is **merged (cumulative), not overwritten**: duplicate metadata keys across base + `extend` are combined into an array.