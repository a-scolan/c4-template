Invalid.

Containment is modeled by nesting, not by a relationship, so `cloud -> backend 'contains traffic'` is invalid because parent-child elements cannot be connected by a relationship.

```likec4
model {
  user = system 'User'
  cloud = system 'Cloud' {
    backend = container 'Backend'
  }
  user -> cloud 'uses'
}
```