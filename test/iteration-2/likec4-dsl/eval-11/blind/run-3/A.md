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

Merged `port` is `9090` because `extend` merges metadata by key and the later value overrides the earlier one for the same key.