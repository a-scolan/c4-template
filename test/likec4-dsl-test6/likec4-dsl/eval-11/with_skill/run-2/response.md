```likec4
model {
  extend cloud.api {
    metadata {
      port '9090'
      region 'us-east-1'
    }
    health = component 'Health Check'
  }
}
```

`port` holds `['8080', '9090']` in the merged model.
The original `port '8080'` is not overwritten; duplicate metadata keys added via `extend` are merged into an array, while `region 'us-east-1'` is added as a new metadata key.