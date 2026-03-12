Use the existing `Container_Api` kind under your system, for example:

```likec4
model {
  mySystem = System_New 'My System' {
    fileIngestionApi = Container_Api 'File Ingestion API' {
      technology 'Node.js, Fastify'
      description 'Receives file uploads and starts the ingestion workflow.'
    }
  }
}
```

If your system variable already exists, add only the `fileIngestionApi` block inside that existing system.