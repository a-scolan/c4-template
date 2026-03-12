I would split this into three passes instead of forcing everything into one view:

1. Use `create-sequence-view` for the step-by-step upload journey.
2. Use `design-view` only for a companion structural view that keeps parent context and neighbors visible.
3. Use `customize-view` after the structure is correct to highlight critical elements with shared-spec colors.

A good split looks like this.

### 1. Temporal flow: `create-sequence-view`

```likec4
views 'Use Cases' {
  dynamic view upload_flow {
    title 'Upload'

    user -> mySystem.webapp 'Open upload form'
    mySystem.webapp -> mySystem.api 'POST /upload'
    mySystem.api -> mySystem.processingService 'Validate and queue work'
    mySystem.processingService -> mySystem.objectStorage 'Store file'
  }
}
```

### 2. Companion static view: `design-view`

```likec4
views 'C2' {
  view c2_upload_path {
    title 'Upload Path'

    include user
    include mySystem
    include mySystem.webapp
    include mySystem.api
    include mySystem.processingService
    include mySystem.objectStorage

    include -> mySystem.api
    include mySystem.api ->
  }
}
```

### 3. Visual emphasis: `customize-view`

```likec4
view c2_upload_path {
  style * { color muted; opacity 20% }
  style mySystem.webapp, mySystem.api, mySystem.processingService {
    color primary
    opacity 100%
  }
  style mySystem.objectStorage {
    color danger
    opacity 100%
  }
}
```

Why this is the clean LikeC4 approach:
- The step-by-step journey is temporal, so it belongs to `create-sequence-view` in `views 'Use Cases'`.
- The static context view is where `design-view` helps: parent boundary, focus elements, and neighbors.
- The color treatment is a separate concern, so it belongs to `customize-view`, not to the structural design step.

So my recommendation is: sequence first, companion structure second, styling last. That keeps the model clean and avoids turning one diagram into a Swiss Army chainsaw.
