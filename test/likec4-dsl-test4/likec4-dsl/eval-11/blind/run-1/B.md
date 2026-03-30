## Correct `ops.c4` snippet

```likec4
model {
  extend cloud.api {
    metadata { port '9090'; region 'us-east-1' }

    health = component 'Health Check'
  }
}
```

## What value does `port` hold in the merged model?

`port` holds **`["8080", "9090"]`** — an array of both values.

## Why: duplicate metadata keys become arrays, not overwrites

LikeC4 merges `metadata` across `extend` blocks by accumulating duplicate keys into arrays. The original `port '8080'` defined in `base.c4` is **not overwritten**. Instead, the new value `'9090'` added by `extend` is appended, resulting in `port ["8080", "9090"]`. Unique keys (like `region 'us-east-1'`) are simply added as-is. This additive behaviour applies to all `metadata` keys across any number of `extend` blocks in any file.
