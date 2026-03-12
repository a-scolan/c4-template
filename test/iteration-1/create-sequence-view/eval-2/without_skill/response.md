A clean showcase proposal is:

```likec4
views 'Use Cases' {
  dynamic view async_processing_flow of webapp {
    title 'Async Processing Flow'

    include person_external
    include webapp
    include api
    include queue
    include processing_server
    include database

    person_external -> webapp 'Starts the request'
    webapp -> api 'Submits the request'
    api -> queue 'Enqueues background work'
    queue -> processing_server 'Dispatches job for processing'
    processing_server -> database 'Stores processed result'
    api -> webapp 'Returns accepted status'
    webapp -> person_external 'Shows tracking information'
  }
}
```

This keeps the flow initiated by `person_external` and shows `api -> queue -> processing_server` in temporal order using only simple `->` arrows.
