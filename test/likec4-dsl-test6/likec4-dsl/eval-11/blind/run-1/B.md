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

The original `port '8080'` is **overwritten** (not merged as two values), because metadata keys are merged by key and the later `extend` assignment for the same key (`port`) wins. The new `region` key is added, and `health` is added as a nested child component.