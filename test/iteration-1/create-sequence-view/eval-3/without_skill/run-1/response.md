Show the immediate success first, then a bounded retry storyline for the background validator. Do not try to model an infinite loop; dynamic views are ordered narratives, not full state machines. Example:
```likec4
views {
  dynamic view upload_with_tracking_and_retries {
    title "Async upload with immediate tracking and background retries"

    user -> webApp "Upload file"
    webApp -> api "POST /uploads"
    api -> database "Create upload record"
    api -> webApp "202 Accepted + trackingUrl"
    webApp -> user "Display tracking URL"

    api -> jobQueue "Enqueue validation job"
    jobQueue -> validationWorker "Deliver job (attempt 1)"
    validationWorker -> database "Write status: validation_failed"
    validationWorker -> jobQueue "Schedule retry"

    jobQueue -> validationWorker "Deliver job (attempt 2)"
    validationWorker -> database "Write status: validated"
  }
}
```
If retry policy, backoff, or dead-letter handling makes the diagram too busy, split it into two dynamic views: one for the immediate acknowledgment and one for the background validation/retry behavior.
