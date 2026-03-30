Invalid.
Containment is modeled by nesting, not by a relationship.

```likec4
model {
  cloud = system 'Cloud' {
    backend = container 'Backend'
    frontend = container 'Frontend'
    frontend -> backend 'calls'
  }
}
```Invalid.

Containment is modeled by nesting, not by a relationship.

**Smallest valid rewrite:**

```likec4
model {
  user = actor 'User'

  cloud = system 'Cloud' {
    backend = container 'Backend'
  }

  user -> cloud 'uses'
}
```

The parent/child relationship between `cloud` and `backend` is preserved through nesting. The invalid `cloud -> backend` relationship is removed. One valid non-parent/child relationship (`user -> cloud`) is added instead.
