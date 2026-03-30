# `extend` with metadata and nested elements in LikeC4

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

**`port` holds `'9090'`** — the value defined in `ops.c4`.

## Why — overwrite or merge?

In LikeC4, `extend` **overwrites** individual metadata keys, not the entire metadata block. The merge behaviour is key-level:

- Keys present only in the original (`base.c4`) and not re-declared in the extension are **kept** as-is.
- Keys that appear in both the original and the extension are **overwritten** by the extension's value; the original value is lost.
- Keys present only in the extension are **added** to the element.

Since `port` is declared in both `base.c4` (`'8080'`) and `ops.c4` (`'9090'`), the extension **overwrites** the original. The `region 'us-east-1'` key, which only appears in the extension, is simply added.

### Final merged state of `cloud.api`

| Metadata key | Value     | Origin            |
|--------------|-----------|-------------------|
| `port`       | `'9090'`  | `ops.c4` (overwrites `base.c4`) |
| `region`     | `'us-east-1'` | `ops.c4` (added)  |

The nested element `health = component 'Health Check'` is also added to `cloud.api` by the extension.

> **Summary:** `port '8080'` is **overwritten** (not merged) by `port '9090'`. LikeC4 does not accumulate multiple values for the same metadata key; the last `extend` wins per key.
