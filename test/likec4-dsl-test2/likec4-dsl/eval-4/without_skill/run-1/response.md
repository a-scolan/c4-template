That styling should live in the **view**, not in the shared model/spec, because your requirement is explicitly **view-specific**: only one view should highlight `cloud.backend.*` while everything else stays muted. Put shared styling in the model/spec only if you want the same emphasis reused across multiple views.

Minimal snippet:

views {
  view cloud_backend_focus of cloud {
    include *

    style * {
      opacity 20%
    }

    style cloud.backend.* {
      opacity 100%
    }
  }
}

If you want, I can also give you the same idea using tags (often more reusable than wildcard ids).
