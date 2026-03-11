Pour ce flux asynchrone, garde une vraie séquence dans `views 'Use Cases'` :

```likec4
views 'Use Cases' {
  dynamic view async_processing_flow {
    title 'Async Processing'

    person_external -> webapp 'Submits request'
    webapp -> api 'POST /jobs'
    api -> queue 'Publish job'
    queue -> processing_server 'Deliver queued work'
    processing_server -> database 'Persist result'
    processing_server -> webapp 'Expose status update'
  }
}
```

Le passage asynchrone reste lisible parce qu'il est raconté étape par étape, avec l'acteur initiateur en tête.