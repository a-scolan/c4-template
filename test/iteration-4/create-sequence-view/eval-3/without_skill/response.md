Do not try to force the whole branch-and-loop story into one overloaded dynamic view. The clean approach is to use two dynamic views.

First, the immediate acknowledgement view:
views {
  dynamic view upload_acknowledgement {
    title 'Async upload acknowledgement'
    include user, webApp, api, jobQueue

    user -> webApp 'Upload file'
    webApp -> api 'POST /uploads'
    api -> jobQueue 'Enqueue validation job'
    api -> webApp '202 Accepted + tracking URL'
    webApp -> user 'Show tracking URL'
  }
}

Second, the background retry view:
views {
  dynamic view validation_retries {
    title 'Background validation with retries'
    include jobQueue, validationWorker, database

    jobQueue -> validationWorker 'Deliver validation job'
    validationWorker -> database 'Write validated result'
    validationWorker -> jobQueue 'Requeue job on failure (retry up to N times)'
  }
}

If you must keep a single view, summarize retries with one requeue step instead of drawing every retry iteration.
