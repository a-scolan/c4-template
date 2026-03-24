For a step-by-step upload journey, do **not** use a C1/C2/C3 static view. The right LikeC4 approach is a `dynamic view` in `views 'Use Cases'`, because order matters more than structure here.

```likec4
views 'Use Cases' {
  dynamic view uploadJourney {
    title 'Upload Journey'

    user -> browser 'Select file'
    browser -> corePlatform.webApp 'Open upload page'
    corePlatform.webApp -> corePlatform.api 'POST /uploads'
    corePlatform.api -> corePlatform.uploadService 'Validate request'
    corePlatform.uploadService -> corePlatform.objectStorage 'Store file'
  }
}
```

For color highlighting, keep that as a second pass: tag the critical elements and style that tag, rather than forcing the sequence into a static view. In short: dynamic view for the journey, styling/tags for the emphasis.
