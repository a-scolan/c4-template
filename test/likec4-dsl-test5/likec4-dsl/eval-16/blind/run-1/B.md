Invalid.
Containment is modeled by nesting, not by a relationship.

```likec4
model {
  cloud = system 'Cloud' {
    backend = container 'Backend'
    cache = container 'Cache'
    backend -> cache 'reads/writes'
  }
}
```
# Evaluation Response

Invalid.

Containment is modeled by nesting, not by a relationship; a parent element cannot have an explicit `->` relationship to its own child.

## Smallest valid rewrite

```likec4
model {
  customer = actor 'Customer'
  cloud = system 'Cloud' {
    backend = container 'Backend'
  }
  customer -> cloud 'uses'
}
```

The hierarchy (`backend` nested inside `cloud`) is unchanged. The single added relationship is between an external actor and the system — a valid non-parent/child relationship.
