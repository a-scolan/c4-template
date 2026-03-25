Invalid. In LikeC4, `backend` is already contained by `cloud` because it is nested inside the `cloud` block. Containment is modeled by hierarchy, not by a relationship like `cloud -> backend`. A corrected minimal pattern is:

model {
  user = person 'User'
  cloud = system 'Cloud' {
    backend = container 'Backend'
  }
  user -> backend 'uses'
}

This keeps the hierarchy (`backend` inside `cloud`) and adds a valid relationship elsewhere.
