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

In the merged model, `port` is **`9090`**.

Why: metadata entries are merged by key, and the later value for the same key replaces the earlier one. So the original `port '8080'` is **overwritten**, not combined, while `region 'us-east-1'` is added as a new metadata entry.