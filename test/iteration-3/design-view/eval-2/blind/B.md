For an upload journey, split the work into three parts:

1. `design-view`: create only a companion structural view so readers can see the parent boundary, the upload focus, and its neighbors. For example:
views 'C3' {
  view c3_uploadService {
    title 'Upload Service'
    include corePlatform
    include corePlatform.uploadService
    include -> corePlatform.uploadService
    include corePlatform.uploadService ->
  }
}

2. `create-sequence-view`: use this for the step-by-step upload journey itself, because order and time are the main concern.
3. `customize-view`: apply colors and highlighting after the structural and dynamic views are correct.

So the clean LikeC4 approach is: one small structural view from `design-view`, the actual journey in `views 'Use Cases'` via `create-sequence-view`, and visual emphasis layered on later via `customize-view`.
