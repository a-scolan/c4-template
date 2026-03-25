No — this is invalid in LikeC4.

`cloud -> backend` tries to create a relationship between a parent element and its own child. Containment is modeled by nesting, not by a relationship.

A corrected minimal pattern (same hierarchy, valid relationship elsewhere):

```likec4
model {
  user = person 'User'

  cloud = system 'Cloud' {
    backend = container 'Backend'
  }

  user -> cloud.backend 'uses'
}
```