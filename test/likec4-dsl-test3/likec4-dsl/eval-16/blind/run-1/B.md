No — that relationship is **invalid**.

In LikeC4, you cannot create relationships between a parent element and its direct child. Here, `cloud` is the parent of `backend`, so `cloud -> backend` is not allowed.

A minimal valid pattern is to keep the hierarchy and add relationships between non-parent/child elements, for example from an external actor to `backend`:

```likec4
model {
  user = actor 'User'

  cloud = system 'Cloud' {
    backend = container 'Backend'
  }

  user -> cloud.backend 'uses'
}
```