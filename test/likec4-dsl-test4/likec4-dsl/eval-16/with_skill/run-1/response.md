Invalid.

Containment is modeled by nesting, not by a relationship; parent-to-child relationships are not allowed in LikeC4.

Smallest valid rewrite — hierarchy unchanged, one valid non-parent/child relationship added:

```likec4
model {
  customer = actor 'Customer'
  cloud = system 'Cloud' {
    backend = container 'Backend'
  }
  customer -> cloud.backend 'uses'
}
```
