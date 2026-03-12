Show it as two dynamic views, not one overloaded pseudo-workflow. A dynamic view works best as a clear scenario slice, not as a full `if/else` diagram.

```likec4
views 'Use Cases' {
  dynamic view upload_request_accepted of webapp {
    title 'Upload Accepted'

    include user
    include webapp
    include api
    include queue

    user -> webapp 'Uploads file'
    webapp -> api 'Sends upload request'
    api -> queue 'Queues validation job'
    api -> webapp 'Returns tracking URL'
    webapp -> user 'Shows tracking URL immediately'
  }

  dynamic view upload_validation_retries of processing_server {
    title 'Upload Validation Retries'

    include queue
    include processing_server
    include database

    queue -> processing_server 'Starts validation'
    processing_server -> database 'Reads upload metadata'
    processing_server -> queue 'Requeues validation after failure'
    queue -> processing_server 'Retries validation'
    processing_server -> database 'Stores final validation result'
  }
}
```

Keep the first view explicitly initiated by `user`. Put the background retry loop in its own dynamic view, and keep every interaction as a simple `->` step with an action label. That shows immediate success and retry behavior without turning one dynamic view into a pseudo `if/else` model.
