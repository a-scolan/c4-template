One reasonable LikeC4 proposal is:
views {
  dynamic view async_processing_flow {
    title 'Async processing flow'
    include externalUser, webApp, api, jobQueue, processingWorker, database

    externalUser -> webApp 'Start the upload'
    webApp -> api 'POST /uploads'
    api -> jobQueue 'Enqueue processing job'
    api -> webApp '202 Accepted + tracking URL'
    webApp -> externalUser 'Show tracking URL'
    jobQueue -> processingWorker 'Deliver queued job'
    processingWorker -> database 'Persist processing result'
  }
}
For the underlying model, the queue hops should be backed by `async` relationships.
