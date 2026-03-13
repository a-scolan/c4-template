Inside the existing system block, add:
fileIngestionApi = Container_Api 'File Ingestion API' {
  technology 'Node.js, Fastify'
  description 'Receives uploaded files and starts the ingestion workflow.'
}
This reuses the shared `Container_Api` kind, keeps a camelCase variable name, and stays focused on the element declaration.
