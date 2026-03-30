This happens because LikeC4 resolves references against the model namespace/scope, not by file-local aliases: files are merged into one model, and `backend.api` is interpreted as a path from a top-level `backend` element (which does not exist), so it is unresolved.

Use fully qualified names from the root element:

```likec4
cloud.backend.api -> cloud.db
```# Cross-File Reference Resolution in LikeC4

## Why `backend.api -> cloud.db` Fails

In LikeC4, **only root-level (top-level) element names become globally accessible identifiers** across files. Nested element names — those declared inside a parent element's braces — are local aliases scoped to their declaration context. They do not enter the global namespace.

Given `base.c4`:

```c4
cloud = system {
  backend = container {
    api = service
  }
}
```

The globally available identifier is **`cloud`** only. The names `backend` and `api` are nested aliases; they have no existence in the global scope that `ops.c4` can see.

When `ops.c4` contains:

```c4
backend.api -> cloud.db
```

The LikeC4 resolver tries to find a **root-level element named `backend`** in the global scope. No such root element exists — `backend` is a child of `cloud`, not a root declaration. Resolution fails immediately with "unresolved reference" because the lookup never reaches into `cloud`'s children.

## Root Cause Summary

| Name | Declared as | Globally visible? |
|------|-------------|-------------------|
| `cloud` | root element | **Yes** |
| `backend` | child of `cloud` | No — local alias only |
| `api` | child of `backend` | No — local alias only |

The dot notation `backend.api` is interpreted as *"look up root element `backend`, then navigate to child `api`"* — not as a relative path continuation from `cloud`.

## Corrected Cross-File Relationship (FQNs)

Use the **Fully Qualified Name** starting from the root element:

```c4
cloud.backend.api -> cloud.db
```

- `cloud.backend.api` — navigates from the root `cloud` → its child `backend` → its child `api`
- `cloud.db` — navigates from the root `cloud` → its child `db`

Both sides of the relationship now start from a globally-known root identifier, so the resolver can unambiguously locate the elements across files.
