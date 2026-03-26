Use **two dynamic views** (or two clearly separated scenarios) so you show immediate success and retry behavior without forcing unsupported branching semantics.

```likec4
dynamicView upload_immediate_ack {
  title "Upload request - immediate acknowledgement"

  include externalUser
  include webApp
  include api
  include jobQueue

  externalUser -> webApp "Submit upload"
  webApp -> api "POST /uploads"
  api -> jobQueue "Enqueue validation job"
  api -> webApp "202 Accepted + trackingUrl"
  webApp -> externalUser "Display tracking URL"
}
```

```likec4
dynamicView upload_background_validation_with_retries {
  title "Background validation with retries"

  include jobQueue
  include validationWorker
  include database
  include deadLetterQueue

  jobQueue -> validationWorker "Attempt #1"
  validationWorker -> database "Validate + write result"
  database -> validationWorker "Temporary failure"
  validationWorker -> jobQueue "Requeue (retry #2)"

  jobQueue -> validationWorker "Attempt #2"
  validationWorker -> database "Validate + write result"
  database -> validationWorker "Temporary failure"
  validationWorker -> jobQueue "Requeue (retry #3)"

  jobQueue -> validationWorker "Attempt #3"
  validationWorker -> database "Validate + write result"
  database -> validationWorker "Failure persists"
  validationWorker -> deadLetterQueue "Move to DLQ / mark failed"
}
```

Practical rule: dynamic views are linear message narratives. For alternatives (success vs retries vs terminal failure), model multiple scenarios instead of one branched mega-diagram.