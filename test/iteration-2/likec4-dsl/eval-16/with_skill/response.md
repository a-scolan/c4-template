**Invalid.** The relationship `cloud -> backend` is a parent-to-child relationship. The skill states explicitly: *'Relationships exist between any pair of elements, but not between parent-child elements.'* `backend` is nested inside `cloud`, so a direct relationship between them is forbidden.

**Corrected minimal pattern** — keep the hierarchy and add a valid relationship between two non-parent-child elements:

```likec4
model {
  cloud = system 'Cloud' {
    frontend = container 'Frontend'
    backend = container 'Backend'

    frontend -> backend 'sends requests'
  }
}
```

`frontend` and `backend` are siblings (both children of `cloud`), so a relationship between them is valid.
