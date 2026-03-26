Use one dynamic view in `views 'Use Cases'` and encode both the immediate return path and the background retry loop as explicit steps.

```likec4
views 'Use Cases' {
  dynamic view asyncUploadValidationLifecycle {
    title 'Async Upload Validation Lifecycle'
    user -> webApp 'Sends upload'
    webApp -> api 'POST /upload'
    api -> jobQueue 'Queues validation task'
    api -> webApp 'Responds with tracking URL'
    webApp -> user 'Shows tracking URL immediately'

    jobQueue -> validationWorker 'Processes validation task'
    validationWorker -> database 'Stores success outcome'

    validationWorker -> retryScheduler 'Signals failed attempt'
    retryScheduler -> jobQueue 'Schedules retry attempt'
    jobQueue -> validationWorker 'Dispatches retry task'
    validationWorker -> database 'Stores post-retry outcome'
  }
}
```

Critical anti-pattern: do not use parent → own-child arrows when modeling retry steps.
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
