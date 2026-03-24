Use `Container_Api` under the existing system, not a custom kind. Paste this inside the existing system block:

ingestionApi = Container_Api 'File Ingestion API' {
  technology 'Node.js, Fastify'
  description 'Receives uploaded files and starts the file ingestion workflow.'
}

That reuses the shared container kind and keeps the placement correct at C2.
