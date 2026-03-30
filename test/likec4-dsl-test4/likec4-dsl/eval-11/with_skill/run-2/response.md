## `ops.c4` snippet

```likec4
model {
  extend cloud.api {
    metadata { port '9090'; region 'us-east-1' }

    health = component 'Health Check'
  }
}
```

## What value does `port` hold in the merged model?

`port` becomes the **array `["8080", "9090"]`**.

The original `port '8080'` is **not overwritten** — it is **merged**. LikeC4's metadata merge rule is: when the same key appears in both the original element and in an `extend` block, the values are combined into an array. The original value comes first, the extended value second.

- `port` → `["8080", "9090"]` (merged, both values preserved)
- `region` → `"us-east-1"` (new key, no conflict — scalar string)
- `health` child element is added to `cloud.api` as a direct nested component.
