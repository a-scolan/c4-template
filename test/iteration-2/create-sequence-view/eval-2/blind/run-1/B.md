Yes—this should be modeled as a dynamic sequence in `views 'Use Cases'`.

```likec4
views 'Use Cases' {
  dynamic view asyncProcessingFlow {
    title 'Async Processing Flow'
    externalUser -> webApp 'Submits request'
    webApp -> api 'POST /process'
    api -> jobQueue 'Enqueues job'
    jobQueue -> processingWorker 'Delivers job'
    processingWorker -> database 'Stores processing result'
    api -> webApp 'Returns accepted/tracking'
  }
}
```

Anti-pattern to avoid: parent → own-child interactions in this dynamic view.
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
