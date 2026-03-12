Model this as two small dynamic views instead of one overloaded pseudo-`if/else` diagram.

A dynamic view works best when it tells one clear time-ordered story. For this case:
- one view shows the immediate user-facing success path
- a second view shows the background validation and retry behavior

That keeps the initiating actor explicit, avoids turning the diagram into a logic tree, and stays within plain `->` sequence steps.

```likec4
views 'Use Cases' {
  dynamic view upload_submission {
    title 'Upload Submission'

    user -> webApp 'Uploads file'
    webApp -> api 'POST /uploads'
    api -> jobQueue 'Queue validation job'
    api -> webApp 'Return tracking URL'
    webApp -> user 'Display tracking URL immediately'
  }

  dynamic view validation_retry {
    title 'Validation Retry'

    retryScheduler -> validationWorker 'Start validation attempt'
    validationWorker -> objectStorage 'Read uploaded file'
    validationWorker -> database 'Store validation status'
    validationWorker -> jobQueue 'Requeue failed validation when retry is needed'
    jobQueue -> retryScheduler 'Trigger next retry window'
    validationWorker -> database 'Persist final success or failure outcome'
  }
}
```

The important idea is not to cram immediate acknowledgment and every retry branch into one giant sequence. Use one linear dynamic view per story: the user-triggered submission flow, then the async retry flow.