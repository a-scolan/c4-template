Invalid.

Containment is modeled by nesting, not by a relationship.

`cloud -> backend 'contains traffic'` is invalid because it defines a relationship from a parent element to its direct child.

```likec4
model {
  ops = system 'Ops'

  cloud = system 'Cloud' {
    backend = container 'Backend'
  }

  ops -> cloud 'monitors'
}
```
