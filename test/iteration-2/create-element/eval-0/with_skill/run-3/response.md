# Add API Container for File Ingestion

**Recommended kind:** `Container_Api`  
**Parent hierarchy:** `System_New → Container_Api`

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

`Container_Api` is the declared shared kind that fits — you do not need to invent a new kind.

**Optional enrichments:** add `icon tech:nodejs`, a `link` to the runbook, or a `#external` tag if applicable.  
**Next:** arrows → `create-relationship`, views → `design-view`.
