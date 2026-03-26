Perfect fit for a dynamic view under `views 'Use Cases'`:

```likec4
views 'Use Cases' {
  dynamic view externalRequestAsyncFlow {
    title 'External Request Async Flow'
    externalUser -> webApp 'Starts processing request'
    webApp -> api 'Sends payload'
    api -> jobQueue 'Queues background work'
    jobQueue -> processingWorker 'Dispatches job'
    processingWorker -> database 'Persists output'
    api -> webApp 'Acknowledges request'
  }
}
```

Critical anti-pattern: avoid parent-to-own-child calls when describing sequence steps.
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
