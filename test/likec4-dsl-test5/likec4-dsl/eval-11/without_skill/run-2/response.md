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

The original `port '8080'` is **overwritten (replaced)** by the `extend` block value for the same metadata key. Metadata is merged by key, so:
- `port`: replaced by the latest value (`'9090'`)
- `region`: added as a new key
# LikeC4 `extend` and Metadata Merging

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

`port` holds **`'9090'`**.

## Why — overwritten or merged?

The original `port '8080'` is **overwritten**, not merged.

LikeC4 metadata is a key-value map; each key must be unique per element. When `extend cloud.api` supplies `port '9090'`, that new value replaces the existing `port '8080'` declared in `base.c4`. There is no union or list-append semantics for duplicate metadata keys.

The `region 'us-east-1'` key did not exist on `cloud.api` before, so it is simply **added** (a true additive merge).

The nested element `health = component 'Health Check'` is likewise **added** as a new child of `cloud.api`.

### Summary table

| Item | Behavior | Final value |
|---|---|---|
| `port` | Overwritten | `'9090'` |
| `region` | Added (new key) | `'us-east-1'` |
| `health` component | Added (new child) | present |
