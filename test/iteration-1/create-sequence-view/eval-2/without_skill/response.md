For the async flow, make the queue handoff explicit and show the user-facing acknowledgment before the worker continues in the background:
```likec4
views {
  dynamic view async_processing {
    title "Async flow: external user to processing worker"

    externalUser -> webApp "Start request"
    webApp -> api "Submit job"
    api -> jobQueue "Enqueue work"
    api -> webApp "202 Accepted + tracking id"
    webApp -> externalUser "Show accepted state"

    jobQueue -> processingWorker "Deliver queued job"
    processingWorker -> database "Persist result"
  }
}
```
If you want the shortest possible version, the essential chain is `externalUser -> webApp -> api -> jobQueue -> processingWorker -> database`.
