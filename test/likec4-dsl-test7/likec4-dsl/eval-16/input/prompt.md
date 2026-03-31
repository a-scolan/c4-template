Is this relationship valid in LikeC4? Start your answer with `Valid.` or `Invalid.` exactly.
```likec4
model {
  cloud = system 'Cloud' {
    backend = container 'Backend'
    cloud -> backend 'contains traffic'
  }
}
```
If invalid, explicitly say in one sentence that containment is modeled by nesting, not by a relationship. Then provide the smallest valid rewrite that keeps the hierarchy unchanged and adds exactly one valid non-parent/child relationship elsewhere.
