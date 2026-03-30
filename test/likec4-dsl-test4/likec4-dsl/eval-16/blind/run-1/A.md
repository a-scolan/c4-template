Invalid.

In LikeC4, containment is modeled by nesting elements inside each other, not by a relationship between parent and child.

```likec4
model {
  cloud = system 'Cloud' {
    backend = container 'Backend'
  }
  actor = actor 'User'
  actor -> backend 'uses'
}
```
