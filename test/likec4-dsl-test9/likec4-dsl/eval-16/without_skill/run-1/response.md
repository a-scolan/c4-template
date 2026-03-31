Invalid.

Containment is modeled by nesting, not by a relationship.

Smallest valid rewrite:

```likec4
model {
  user = person 'User'

  cloud = system 'Cloud' {
    backend = container 'Backend'
  }

  user -> cloud.backend 'Uses'
}
```