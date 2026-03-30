Invalid.

Containment is modeled by nesting, not by a relationship.

In the original snippet, `cloud -> backend 'contains traffic'` is invalid because `backend` is a direct child (nested element) of `cloud`. The LikeC4 DSL explicitly prohibits relationships between parent and child elements — the hierarchy is already expressed by the nesting itself.

**Smallest valid rewrite:**

```likec4
model {
  cloud = system 'Cloud' {
    backend = container 'Backend'
    frontend = container 'Frontend'
    frontend -> backend 'calls'
  }
}
```

Changes made:
- Removed the invalid parent→child relationship `cloud -> backend`.
- Added a sibling container `frontend` inside `cloud` (hierarchy unchanged — `backend` is still nested in `cloud`).
- Added exactly one valid relationship `frontend -> backend 'calls'` between two sibling elements (neither is an ancestor/descendant of the other).
