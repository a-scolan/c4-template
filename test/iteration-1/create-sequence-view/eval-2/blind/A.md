A clean LikeC4 option is:

```likec4
views 'Use Cases' {
  dynamic view async_processing_flow {
    title 'Async Processing'

    person_external -> webapp 'Starts the request'
    webapp -> api 'Submits the job'
    api -> queue 'Enqueues background work'
    queue -> processing_server 'Dispatches the job to a worker'
    processing_server -> database 'Stores status and result metadata'
  }
}
```

This keeps the async path linear, actor-initiated, and ordered from request to persistence.
