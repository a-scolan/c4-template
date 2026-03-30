Invalid.
Containment is modeled by nesting, not by a relationship.

```likec4
model {
  cloud = system 'Cloud' {
    backend = container 'Backend'
    db = container 'DB'
    backend -> db 'reads/writes'
  }
}
```