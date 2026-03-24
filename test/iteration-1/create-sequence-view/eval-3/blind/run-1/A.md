The cleanest way is to use two short dynamic views in `views 'Use Cases'`: one for the immediate acknowledgement, and one for the background retry loop. That keeps each sequence linear and readable instead of forcing branching into one oversized view.

Assuming IDs such as `externalUser`, `webApp`, `api`, `objectStorage`, `jobQueue`, `validationWorker`, and `primaryDatabase` exist:

views 'Use Cases' {
  dynamic view uploadAccepted {
    title 'Upload Accepted'
    externalUser -> webApp 'Uploads file'
    webApp -> api 'POST /upload'
    api -> objectStorage 'Stores file'
    api -> primaryDatabase 'Creates tracking record'
    api -> webApp 'Returns tracking URL'
  }

  dynamic view uploadValidationRetry {
    title 'Upload Validation Retry'
    api -> jobQueue 'Queues validation'
    jobQueue -> validationWorker 'Delivers job'
    validationWorker -> primaryDatabase 'Marks validating'
    validationWorker -> jobQueue 'Requeues job'
    jobQueue -> validationWorker 'Redelivers job'
    validationWorker -> primaryDatabase 'Updates final status'
  }
}

Critical anti-pattern: do not try to encode retries, branching, and parent -> own-child hops in one dynamic view. Keep each view action-focused and ordered.
