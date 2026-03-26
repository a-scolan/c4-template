Use the built-in `container` kind under your existing system. Keep it minimal, for example:

```likec4
model {
  yourSystem = system "Your System" {
    fileIngestionApi = container "File Ingestion API"
  }
}
```

If `yourSystem` already exists elsewhere, only add the inner `fileIngestionApi = container ...` line inside it.