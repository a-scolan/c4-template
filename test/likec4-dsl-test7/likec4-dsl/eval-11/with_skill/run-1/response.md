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

`port` in the merged model is **an array with both values**: `["8080", "9090"]`.

The original `port "8080"` is **not overwritten**. For `extend`, metadata is merged; when the same metadata key appears more than once, LikeC4 keeps both values (duplicate keys become an array).