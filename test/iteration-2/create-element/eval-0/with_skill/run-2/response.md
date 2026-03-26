# Add API Container for File Ingestion

**Kind:** `Container_Api`  
**Parent:** place inside the existing file ingestion system

## Minimal Declaration

```likec4
model {
  fileIngestionSystem = System_New 'File Ingestion System' {

    ingestionApi = Container_Api 'Ingestion API' {
      technology 'Node.js, Fastify'
      description 'Receives uploaded files and triggers the ingestion workflow.'
    }

  }
}
```

Use `Container_Api` from the shared spec — it is the right kind for any internal HTTP/REST API container. No custom kind needed.

**If you also need:**
- Relationship arrows → `create-relationship`
- A container view → `design-view`
