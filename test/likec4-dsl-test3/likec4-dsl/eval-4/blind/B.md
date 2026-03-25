Use **view-level styling** for this.

- Put stable, reusable semantics in the model/spec (kinds, tags, default styles).
- Put "highlight only `cloud.backend.*` in this one diagram" in the **view**, because it is presentation-specific.

```likec4
view cloud_backend_focus of cloud {
  include *

  // mute everything
  style * {
    opacity 20
  }

  // highlight only backend subtree
  style cloud.backend.* {
    opacity 100
  }
}
```