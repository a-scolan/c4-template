Assuming the model already contains `externalUser`, `webApp`, `api`, `jobQueue`, `processingWorker`, and `database`, I would write the dynamic view like this:
views 'Use Cases' {
  dynamic view async_processing_flow {
    title 'Async Processing Flow'

    include externalUser
    include webApp
    include api
    include jobQueue
    include processingWorker
    include database

    externalUser -> webApp 'Submit request'
    webApp -> api 'POST /jobs'
    api -> jobQueue 'Publish job'
    jobQueue -> processingWorker 'Deliver job'
    processingWorker -> database 'Write result/status'
  }
}

In the model, use `calls` for the first two hops, `async` for `api -> jobQueue` and `jobQueue -> processingWorker`, and `writes` for `processingWorker -> database`. If you still need to create the elements, the repo's closest kinds are `Actor_Person`, `Container_Webapp`, `Container_Api`, `Container_Queue`, `Container_ProcessingServer`, and `Container_Database`.
