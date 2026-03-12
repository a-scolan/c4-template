Inside the parent system block, add this minimal declaration:

```likec4
fileIngestionApi = Container_Api 'File Ingestion API' {
  technology 'Node.js, Express'
  description 'Receives files and exposes ingestion endpoints'
}
```

This reuses the existing `Container_Api` kind and keeps the change limited to the element declaration.