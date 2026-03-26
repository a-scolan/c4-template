Model both immediate acknowledgement and retry in one ordered dynamic flow inside `views 'Use Cases'`.

```likec4
views 'Use Cases' {
  dynamic view uploadTrackingAndRetries {
    title 'Upload Tracking and Background Retries'
    user -> webApp 'Uploads content'
    webApp -> api 'Submits upload'
    api -> jobQueue 'Enqueues validation'
    api -> webApp 'Returns tracking URL now'
    webApp -> user 'Shows tracking URL'

    jobQueue -> validationWorker 'Starts async validation'
    validationWorker -> database 'Writes validation success'

    validationWorker -> retryScheduler 'Requests retry after failure'
    retryScheduler -> jobQueue 'Requeues failed validation'
    jobQueue -> validationWorker 'Runs retry attempt'
    validationWorker -> database 'Writes final validation state'
  }
}
```

Anti-pattern to avoid: mixing static structure details instead of showing temporal step order.
## Async Upload with Immediate Success and Retry – Splitting Dynamic Views

A single dynamic view **cannot branch or loop** — do not try to show both the immediate response path and the retry logic in one view. Split them into two separate dynamic views.

```likec4
views 'Use Cases' {
  dynamic view uploadImmediateResponse {
    title 'Upload – Immediate Response'
    user -> webApp 'Uploads file'
    webApp -> api 'POST /upload'
    api -> jobQueue 'Enqueues processing job'
    api -> webApp 'Returns 202 + tracking URL'
    webApp -> user 'Shows tracking URL'
  }

  dynamic view uploadBackgroundValidation {
    title 'Upload – Background Validation & Retry'
    jobQueue -> processingWorker 'Delivers job'
    processingWorker -> validationService 'Validates file'
    validationService -> processingWorker 'Returns validation error'
    processingWorker -> jobQueue 'Re-enqueues with backoff'
    jobQueue -> processingWorker 'Retries job'
    processingWorker -> objectStorage 'Stores validated file'
    processingWorker -> database 'Updates upload status'
  }
}
```

**Why split?**
- Dynamic views are **linear sequences** — they have no branching or loop constructs.
- One view per scenario keeps each path readable independently.
- The retry view starts from `jobQueue -> processingWorker` because user interaction is already complete.

**Anti-pattern to avoid:**
```likec4
// ❌ Don't annotate branching inline
api -> webApp 'Returns 202 [if success] or 500 [if fail]'
```
Create one view per distinct outcome path instead.
