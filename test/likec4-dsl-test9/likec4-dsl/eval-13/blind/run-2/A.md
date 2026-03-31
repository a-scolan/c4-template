## Corrected snippet

```likec4
model {
  api = service 'API' #critical {
    technology 'Node.js'
  }
}
```

## Why the original is invalid

`technology 'Node.js'` is valid inside the element body, but `#critical` is not a valid standalone statement there.

In LikeC4, `#critical` is a tag annotation, and tags must be attached to the element declaration itself. Moving the tag onto the declaration line fixes the syntax while keeping the same element kind and both original fields.