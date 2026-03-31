Invalid.
Containment is modeled by nesting, not by a relationship.

```likec4
model {
  user = person 'User'

  cloud = system 'Cloud' {
    backend = container 'Backend'
  }

  user -> backend 'uses'
}
```