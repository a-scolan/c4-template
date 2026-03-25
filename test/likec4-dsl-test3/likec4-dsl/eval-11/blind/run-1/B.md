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

Why: `extend cloud.api` augments the existing element, and when the same metadata key (`port`) is set again in the extension, the extension value overrides the original one (`8080`). The new `region` key is added, and `health` is added as a nested child under `cloud.api`.