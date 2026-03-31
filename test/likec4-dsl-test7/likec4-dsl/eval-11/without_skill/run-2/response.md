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

In the merged model, `port` is **`'9090'`**.

The original `port '8080'` from `base.c4` is **overwritten (replaced)**, not merged as multiple values, because both definitions set the same metadata key (`port`) on the same element (`cloud.api`). The new key `region 'us-east-1'` is added, and the nested component `health` is added under `cloud.api`.
