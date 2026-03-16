view c2_api_docs extends c2 {
  link https://intranet.example/specs/c2

  style * {
    opacity 30%
  }

  style * where tag is #Api {
    color modern
    opacity 100%
  }
}

This stops at view-level customization: layout, emphasis, and links on top of the existing view. Creating or changing model elements, relationships, tags, or the target detail view itself is outside scope.
