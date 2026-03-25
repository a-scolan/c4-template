Use **view-level styling** for this.

- Put styling in the **view** when the emphasis is specific to one diagram.
- Put styling in the **model/spec** only when you want the same rule reused across many views.

Minimal LikeC4 snippet:

```likec4
view cloud_backend_focus of cloud {
  include cloud.*

  style * {
    opacity 20
  }

  style cloud.backend.* {
    opacity 100
  }
}
```