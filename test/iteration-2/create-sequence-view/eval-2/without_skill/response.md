Here is a straightforward dynamic view for that async path:

```likec4
views 'Use Cases' {
  dynamic view asyncProcessingFlow {
    title 'Async Processing Flow'

    externalUser -> webApp 'Start request'
    webApp -> api 'Submit work item'
    api -> jobQueue 'Publish processing job'
    jobQueue -> processingWorker 'Deliver queued job'
    processingWorker -> database 'Store processing result'
    processingWorker -> webApp 'Publish completion state'
    webApp -> externalUser 'Show accepted or completed status'
  }
}
```