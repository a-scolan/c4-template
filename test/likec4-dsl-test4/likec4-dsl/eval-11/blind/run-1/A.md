# ops.c4 snippet and metadata merge behaviour

## Correct `ops.c4` snippet

```likec4
extend cloud.api {
  metadata {
    port '9090'
    region 'us-east-1'
  }
  health = component 'Health Check'
}
```

## What value does `port` hold in the merged model?

**`port` holds `'9090'`.**

## Why — overwritten or merged?

In LikeC4, when two `metadata` blocks define the **same key**, the last definition wins — i.e., the value is **overwritten**, not merged.  
The `extend` block in `ops.c4` is processed after `base.c4`, so its `port '9090'` replaces the original `port '8080'`.

- `region 'us-east-1'` is a **new** key, so it is simply added to the element's metadata.
- `health` is a **new nested element** added to `cloud.api`'s children.

Final effective metadata for `cloud.api`:

| Key    | Value       | Origin  |
|--------|-------------|---------|
| port   | `'9090'`    | ops.c4 (overwrites base.c4) |
| region | `'us-east-1'` | ops.c4 (added) |
