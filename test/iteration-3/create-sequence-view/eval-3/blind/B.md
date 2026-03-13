Keep the dynamic view linear and bounded:

1. Show the immediate acknowledgement first:
   `user -> webApp 'Upload file'`
   `webApp -> api 'POST /uploads'`
   `api -> jobQueue 'Enqueue validation job'`
   `api -> webApp '201 Created + tracking URL'`
   `webApp -> user 'Show tracking URL'`
2. Then show the background work:
   `jobQueue -> validationWorker 'Deliver validation job'`
   `validationWorker -> database 'Write status: validating'`
   `validationWorker -> jobQueue 'Requeue validation (retry 1 of 3)'`
   `jobQueue -> validationWorker 'Redeliver validation job'`
   `validationWorker -> database 'Write status: valid / failed'`

The key is not to model an open-ended loop. Show one representative retry and label it with the policy (`retry 1 of 3`, `with backoff`, and so on). If the single view gets crowded, split it into two dynamic views: one for the immediate acknowledgement and one for the background validation/retry path.
