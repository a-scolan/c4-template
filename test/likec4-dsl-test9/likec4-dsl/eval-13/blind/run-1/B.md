```likec4
model {
  api = service 'API' {
    #critical
    technology 'Node.js'
  }
}
```

The snippet is invalid because, inside a LikeC4 element body, tags must come before properties.

- `#critical` is a tag
- `technology 'Node.js'` is a property

In the original snippet, the property appeared before the tag, which violates the model body ordering rules. The minimal fix is to swap those two lines and keep everything else unchanged.
