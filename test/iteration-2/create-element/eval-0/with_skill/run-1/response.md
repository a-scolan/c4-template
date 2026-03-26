# Add API Container for File Ingestion

**Kind:** `Container_Api`  
**Parent:** the existing system (e.g., `fileIngestionSystem`)

## Minimal Declaration

```likec4
model {
  fileIngestionSystem = System_New 'File Ingestion System' {

    ingestionApi = Container_Api 'Ingestion API' {
      technology 'Node.js, Fastify'
      description 'Receives uploaded files and starts the ingestion workflow.'
    }

  }
}
```

`Container_Api` is the correct shared kind — no custom kind is needed for an internal API container.

**Next steps:**
- Arrows → `create-relationship`
- View showing this container → `design-view`
