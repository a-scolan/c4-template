No — this is invalid.

`cloud -> backend` is a relationship from a parent element to its own nested child. In LikeC4, nesting already expresses hierarchy/containment, and explicit relationships should be between separate elements (typically siblings or elements in different branches), not parent-to-child.

A corrected minimal pattern that keeps the hierarchy and adds a valid relationship elsewhere:

```likec4
model {
  cloud = system 'Cloud' {
    backend = container 'Backend'
  }

  user = system 'User'
  user -> cloud.backend 'sends traffic'
}
```