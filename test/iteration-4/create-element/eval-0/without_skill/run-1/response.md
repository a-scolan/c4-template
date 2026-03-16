Inside the existing system block, start with:
fileIngestionApi = Container_Api 'File Ingestion API'

That is the minimal correct declaration here: it reuses the built-in API container kind and does not invent a custom kind.
