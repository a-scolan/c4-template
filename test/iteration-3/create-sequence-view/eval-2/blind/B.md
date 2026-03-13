This belongs in `views 'Use Cases'`.

views 'Use Cases' {
  dynamic view asyncProcessingFlow {
    title 'Async Processing Flow'
    externalUser -> webApp 'Starts request'
    webApp -> api 'Submits work'
    api -> jobQueue 'Queues processing job'
    jobQueue -> processingWorker 'Delivers queued job'
    processingWorker -> database 'Writes processing result'
  }
}

Anti-pattern to avoid: do not write `api -[async]-> jobQueue`; keep the queue handoff in temporal order with plain `->` arrows.
