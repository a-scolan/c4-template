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

`port` becomes `['8080', '9090']`: the duplicate metadata key is merged (accumulated), not overwritten, so the original `port '8080'` is preserved and combined with the new value.