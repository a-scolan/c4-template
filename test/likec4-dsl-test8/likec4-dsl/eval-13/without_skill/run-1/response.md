```likec4
model {
  api = service 'API' #critical {
    technology 'Node.js'
  }
}
```

The snippet is invalid because `#critical` is tag shorthand, and in LikeC4 it must be attached to the element declaration itself, not used as a standalone statement inside the element body.

`technology 'Node.js'` is already valid, so the minimal fix is simply to move `#critical` onto the `service` declaration line.