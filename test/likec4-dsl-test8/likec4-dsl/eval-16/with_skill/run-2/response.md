Invalid.

Containment is modeled by nesting, not by a relationship.

```likec4
model {
  cloud = system 'Cloud' {
    frontend = container 'Frontend'
    backend = container 'Backend'
    frontend -> backend 'calls'
  }
}
```