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

`port` in the merged model is `['8080', '9090']`.

It is **not overwritten**. It is **merged**: `extend cloud.api` adds metadata to the existing element, and duplicate metadata keys become arrays, so the original `port '8080'` and the added `port '9090'` are both retained. `region 'us-east-1'` is added as a new metadata key.