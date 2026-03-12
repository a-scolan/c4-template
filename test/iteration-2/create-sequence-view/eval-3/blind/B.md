Keep this readable by splitting it into two dynamic views: one for the immediate acknowledgment, and one for the background retry cycle. That keeps causality explicit without turning the diagram into a pseudo `if/else` script.

```likec4
views 'Use Cases' {
  dynamic view uploadAccepted {
    title 'Upload Accepted'

    user -> webApp 'Upload file'
    webApp -> api 'POST upload'
    api -> jobQueue 'Queue validation job'
    api -> webApp 'Return tracking URL'
    webApp -> user 'Show tracking URL'
  }

  dynamic view validationRetry {
    title 'Background Validation Retry'

    scheduler -> jobQueue 'Trigger next validation attempt'
    jobQueue -> validationWorker 'Deliver validation job'
    validationWorker -> fileScanner 'Validate uploaded file'
    validationWorker -> retryQueue 'Requeue failed validation'
    retryQueue -> validationWorker 'Start retry attempt'
    validationWorker -> statusStore 'Persist final validation status'
    validationWorker -> notificationService 'Send completion or failure notice'
  }
}
```