Use two small dynamic views instead of one overloaded branch-heavy diagram. One view shows the immediate user-facing success path, and a second view shows the background validation and retry path. That keeps the initiating actor explicit and avoids turning the diagram into a pseudo `if/else` program.

```likec4
views 'Use Cases' {
  dynamic view upload_submission {
    title 'Upload Submission'

    user -> mySystem.webapp 'Selects a file and starts upload'
    mySystem.webapp -> mySystem.api 'Posts the upload request'
    mySystem.api -> mySystem.queue 'Queues validation work'
    mySystem.api -> mySystem.webapp 'Returns a tracking URL'
    mySystem.webapp -> user 'Shows the tracking URL immediately'
  }

  dynamic view upload_validation_retry {
    title 'Upload Validation Retry'

    scheduler -> mySystem.queue 'Triggers the next validation attempt'
    mySystem.queue -> mySystem.worker 'Dispatches the validation job'
    mySystem.worker -> mySystem.database 'Loads upload metadata'
    mySystem.worker -> mySystem.queue 'Requeues the job after a failure'
    mySystem.worker -> mySystem.database 'Stores final success or failure status'
  }
}
```

If you need even more detail, add a separate view for the terminal failure path rather than stuffing all logic into one dynamic view.
