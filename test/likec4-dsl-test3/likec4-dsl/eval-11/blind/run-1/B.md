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

Why: `extend cloud.api` merges into the existing `cloud.api`, and when the same metadata key is defined again (`port`), the value from the extension overrides the previous one (`'8080'`). The new key (`region`) is added, and `health` is added as a nested child component under `cloud.api`.
