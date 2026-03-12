Under `mySystem`, add:

```likec4
ingestionApi = Container_Api 'File Ingestion API' {
  technology 'Node.js, Fastify'
  description 'Receives file uploads and starts the ingestion workflow'
}
```