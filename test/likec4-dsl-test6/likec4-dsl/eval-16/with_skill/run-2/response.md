Invalid. Relationships between a parent and its child are not valid in LikeC4, and containment is modeled by nesting, not by a relationship.

```likec4
model {
  cloud = system 'Cloud' {
    backend = container 'Backend'
    frontend = container 'Frontend'
    frontend -> backend 'calls'
  }
}
```