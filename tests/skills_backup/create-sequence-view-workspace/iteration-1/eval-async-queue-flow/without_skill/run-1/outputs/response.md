Je mettrais simplement les échanges clés comme ceci :

```likec4
views 'Use Cases' {
  dynamic view async_processing_flow {
    title 'Async Processing'

    api -[async]-> queue
    queue -> processing_server
    processing_server -> database
  }
}
```

Ça suffit pour montrer l'enchaînement technique principal.