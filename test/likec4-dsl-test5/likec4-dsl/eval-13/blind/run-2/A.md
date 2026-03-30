```likec4
model {
  api = service 'API' #critical {
    technology 'Node.js'
  }
}
```

It is invalid because `#critical` is a tag marker and must be attached to the element declaration line, not written as a standalone statement inside the element body.
# Fix: Invalid LikeC4 Snippet

## Why it is invalid

The snippet uses `service` as an element kind, but LikeC4 requires **all element kinds to be declared in a `specification` block** before they can be used in the `model` block. There are no built-in element kinds in LikeC4 — `service`, `actor`, `system`, etc. must all be explicitly declared.

Without the `specification` block, the parser does not recognize `service` as a valid kind, making the entire model block invalid.

## Corrected snippet

```likec4
specification {
  element service
}

model {
  api = service 'API' {
    technology 'Node.js'
    #critical
  }
}
```

The only change is the addition of the `specification { element service }` block. The element definition, its `technology` property, and the `#critical` tag are all left untouched.
