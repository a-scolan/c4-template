Place it in `views 'Use Cases'` and keep the steps short/action-focused:

```likec4
views 'Use Cases' {
  dynamic view queuedProcessing {
    title 'Queued Processing Sequence'
    externalUser -> webApp 'Initiates flow'
    webApp -> api 'Forwards request'
    api -> jobQueue 'Publishes job'
    jobQueue -> processingWorker 'Provides job message'
    processingWorker -> database 'Writes final state'
    api -> webApp 'Returns tracking info'
  }
}
```

Anti-pattern check: don’t model parent → own-child interactions in this flow.
## Async Processing Flow – Dynamic View

This belongs in `views 'Use Cases'`.

```likec4
views 'Use Cases' {
  dynamic view asyncProcessingFlow {
    title 'Async Processing Flow'
    externalUser -> webApp 'Submits request'
    webApp -> api 'Forwards request'
    api -> jobQueue 'Enqueues job'
    api -> webApp 'Returns 202 Accepted'
    webApp -> externalUser 'Returns tracking URL'
    jobQueue -> processingWorker 'Delivers job'
    processingWorker -> database 'Persists result'
  }
}
```

**Notes:**
- `externalUser` is the initiating actor — placed first.
- The synchronous acknowledgment (`202 + tracking URL`) is shown before the async background steps.
- Plain `->` arrows only — no relationship-kind syntax like `-[calls]->`.
- View is inside `views 'Use Cases'` as required for dynamic views.
