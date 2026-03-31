Invalid.

The relationship is invalid because containment is modeled by nesting, not by a relationship.

Smallest valid rewrite:

```likec4
model {
  cloud = system 'Cloud' {
    backend = container 'Backend'
  }

  admin = person 'Admin'
  admin -> cloud 'uses'
}
```