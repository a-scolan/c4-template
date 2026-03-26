Yes—keep it in a single dynamic view under `views 'Use Cases'` by modeling both paths as ordered steps.

```likec4
views 'Use Cases' {
  dynamic view asyncUploadWithRetry {
    title 'Async Upload with Immediate Ack and Retry'
    user -> webApp 'Uploads file'
    webApp -> api 'POST /uploads'
    api -> jobQueue 'Queues validation job'
    api -> webApp 'Returns tracking URL immediately'
    webApp -> user 'Displays tracking URL'

    jobQueue -> validationWorker 'Delivers validation job'
    validationWorker -> database 'Stores validation result (success)'

    validationWorker -> retryScheduler 'Schedules retry on failure'
    retryScheduler -> jobQueue 'Requeues validation job'
    jobQueue -> validationWorker 'Delivers retried job'
    validationWorker -> database 'Stores validation result after retry'
  }
}
```

Critical anti-pattern: do not switch to parent→child arrows when adding retry behavior.
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
