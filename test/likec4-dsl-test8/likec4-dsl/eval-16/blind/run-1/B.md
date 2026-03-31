Invalid. Containment is modeled by nesting, not by a relationship.

```likec4
model {
  monitor = system 'Monitor'

  cloud = system 'Cloud' {
    backend = container 'Backend'
  }

  monitor -> cloud 'observes'
}
```
