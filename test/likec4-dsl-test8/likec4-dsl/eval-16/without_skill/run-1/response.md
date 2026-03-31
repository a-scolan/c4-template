Invalid. Containment is modeled by nesting, not by a relationship.

```likec4
model {
  analytics = system 'Analytics'
  cloud = system 'Cloud' {
    backend = container 'Backend'
  }

  cloud -> analytics 'sends data'
}
```