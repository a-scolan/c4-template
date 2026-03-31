Invalid.

Relationships cannot exist directly between a parent element and its child in LikeC4. Containment is modeled by nesting, not by a relationship.

```likec4
model {
  client = system 'Client'

  cloud = system 'Cloud' {
    backend = container 'Backend'
  }

  client -> cloud 'uses'
}
```