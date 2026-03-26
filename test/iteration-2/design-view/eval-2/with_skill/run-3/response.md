Use **two complementary views**:

1. **Primary**: a dynamic view in `views 'Use Cases'` for the step-by-step upload journey.
2. **Optional companion**: a focused C3 static view for structure/context, with critical elements highlighted via tags/styles.

```likec4
views 'Use Cases' {
  dynamic view uc_uploadJourney {
    title 'Upload Journey'

    customer -> corePlatform.webApplication 'Select file and submit'
    corePlatform.webApplication -> corePlatform.uploadService 'POST /uploads'
    corePlatform.uploadService -> corePlatform.storageAdapter 'Store binary'
    corePlatform.uploadService -> corePlatform.virusScanner 'Scan uploaded file'
    corePlatform.uploadService -> corePlatform.notificationService 'Publish upload-complete event'
  }
}
```

For highlighting critical parts, tag those elements (for example `#critical`) and apply color through styles, instead of overloading the dynamic flow with layout/styling tricks. This keeps order readability high and intent clear.