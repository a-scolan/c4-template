Here is a LikeC4 dynamic view proposal for the async chain `externalUser -> webApp -> api -> jobQueue -> processingWorker -> database`:

```likec4
dynamicView async_upload_flow {
  title "Async upload processing"

  include externalUser
  include webApp
  include api
  include jobQueue
  include processingWorker
  include database

  externalUser -> webApp "Upload request"
  webApp -> api "POST /uploads"
  api -> jobQueue "Enqueue processing job (async)"
  api -> webApp "202 Accepted + trackingId"
  webApp -> externalUser "Show accepted/tracking"

  jobQueue -> processingWorker "Deliver queued job"
  processingWorker -> database "Persist processing result"
}
```

This keeps immediate user feedback and background processing in the same sequence while clearly marking async handoff at the queue.