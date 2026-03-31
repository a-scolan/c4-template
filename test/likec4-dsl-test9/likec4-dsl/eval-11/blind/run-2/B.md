`ops.c4` can extend the existing element like this:

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

In the merged model, `port` holds **`9090`**.

The original `port '8080'` is **overwritten, not merged**. The reason is that `metadata` entries are key-value fields, so when the extension defines the same key (`port`) again, the later value replaces the earlier one. The new key `region 'us-east-1'` is added, and the nested `health` component is appended under `cloud.api`.
