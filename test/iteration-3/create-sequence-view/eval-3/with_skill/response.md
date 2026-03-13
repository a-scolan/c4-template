This still belongs in `views 'Use Cases'`, but do not force the immediate response and the retry loop into one overloaded pseudo `if/else` sequence. Split it into separate dynamic views: one for the user-facing acceptance path, and one for the background retry cycle.

views 'Use Cases' {
  dynamic view uploadAccepted {
    title 'Upload Accepted'
    user -> webApp 'Uploads file'
    webApp -> api 'POST /upload'
    api -> jobQueue 'Queues validation'
    api -> webApp 'Returns tracking URL'
    webApp -> user 'Shows tracking URL'
  }

  dynamic view validationRetry {
    title 'Validation Retry'
    jobQueue -> validationWorker 'Delivers validation job'
    validationWorker -> database 'Checks upload record'
    validationWorker -> jobQueue 'Requeues job after failure'
    jobQueue -> validationWorker 'Delivers retry'
    validationWorker -> database 'Writes final validation status'
  }
}

This keeps the initiating actor explicit for each flow (`user` for the immediate path, `jobQueue` for the async trigger), uses only `->` arrows with action labels, and shows one representative retry cycle instead of turning the dynamic view into full control-flow logic.
