Yes — place it in `views 'Use Cases'` and keep the async sequence explicit with plain `->` arrows.

views 'Use Cases' {
  dynamic view asyncProcessingFlow {
    title 'Async Processing Flow'
    externalUser -> webApp 'Submits request'
    webApp -> api 'POST /process'
    api -> jobQueue 'Queues job'
    jobQueue -> processingWorker 'Delivers job'
    processingWorker -> database 'Stores result'
  }
}

Critical reminder: even for async behavior, use plain `->`, not decorated relationship syntax.
