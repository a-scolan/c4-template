Corrected minimal snippet:

```likec4
model {
  api = service 'API' #critical {
    technology 'Node.js'
  }
}
```

Why invalid: `#critical` cannot appear as a standalone statement inside the body; tags must be attached in supported tag syntax for the element declaration.