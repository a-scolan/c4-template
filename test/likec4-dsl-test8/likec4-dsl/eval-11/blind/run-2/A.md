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

In the merged model, `port` holds **`'9090'`**.

The original `port '8080'` is **overwritten, not merged**. Metadata is merged by key, so adding `region 'us-east-1'` contributes a new metadata entry, while redefining `port` replaces the previous `port` value from `base.c4`.
