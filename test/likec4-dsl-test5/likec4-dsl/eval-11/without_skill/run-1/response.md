Correct `ops.c4` snippet:

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

`port` is **`9090`** in the merged model.

The original `port '8080'` is **overwritten**, not merged. In `extend`, metadata with the same key is replaced by the later value.# LikeC4 `extend` — metadata merging and overwrite behaviour

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

**`port` = `'9090'`**

The original `port '8080'` declared in `base.c4` is **overwritten**, not merged.

## Why

In LikeC4, `extend <fqn> { … }` merges the block's content into the already-declared element.  
For **metadata**, the merge is a **key-level upsert**:

| Key | base.c4 | ops.c4 (extend) | Merged result |
|---|---|---|---|
| `port` | `'8080'` | `'9090'` | `'9090'` ← overwritten |
| `region` | *(absent)* | `'us-east-1'` | `'us-east-1'` ← added |

When the same metadata key appears in both the original declaration and an `extend` block, the **last writer wins**: the value from the `extend` replaces the earlier value.  
Keys that exist only in the original (`region` did not exist in `base.c4`) are preserved unchanged, and keys that exist only in the `extend` block are inserted.

The nested child `health = component 'Health Check'` is simply appended to `cloud.api`'s children; it does not conflict with anything already declared.

### Summary

- `cloud.api.metadata.port` → **`'9090'`** (overwritten by `extend`)
- `cloud.api.metadata.region` → **`'us-east-1'`** (newly added by `extend`)
- `cloud.api.health` → new `component 'Health Check'` child (appended)
