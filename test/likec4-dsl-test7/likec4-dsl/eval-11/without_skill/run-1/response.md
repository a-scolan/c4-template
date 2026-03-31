```likec4
// ops.c4
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

The original `port '8080'` is **overwritten (replaced)**, not merged as multiple values, because `port` is the same metadata key on the same element (`cloud.api`) and the extension provides a new value for that key. The new key `region` is added, and the nested `health` component is added under `cloud.api`.
