# Eval 1 — Splitting a 1200-line `system.c4` progressively

## Core principle

Do not jump from one file to seven files. Split progressively: start with the minimal baseline and add files only when a topic grows large enough to deserve its own home.

## Step 1 — Minimal split (start here)

```
projects/my-project/
  likec4.config.json
  system-model.c4     ← all elements + relationships
  system-views.c4     ← C1/C2/C3 views + index view
```

This is the correct first split for most projects. Move C1/C2/C3 views and the index into `system-views.c4`, everything structural into `system-model.c4`.

## Step 2 — Add focused files only when their topic is substantial

| File | When to add | What goes in it |
|---|---|---|
| `system-sequences.c4` | Dynamic flows exist and are growing | Use Cases (dynamic views) |
| `deployment.c4` | Deployment nodes + instanceOf links are non-trivial | All deployment declarations |
| `deployment-views.c4` | Multiple deployment views needed | Deployment category views |
| `operations.c4` | Operational topology is complex | Operational elements |
| `operations-views.c4` | Multiple operations views needed | Operations category views |

## Required view category rule (hard rule)

Every view except `index` **must** be inside a `views 'FolderName'` block. The `index` view is the only view placed in the root `views { }` block.

```likec4
views {
  // index at root — no folder
  view index extends c1_context { }

  views 'C1' {
    view c1_context { ... }
  }

  views 'C2' {
    view c2_containers of systemName { ... }
  }

  views 'C3' {
    view c3_components of containerName { ... }
  }

  // Dynamic flows — goes in system-sequences.c4
  views 'Use Cases' {
    dynamic view uc_login { ... }
  }

  // Deployment views — goes in deployment-views.c4
  views 'Deployment' {
    view deploy_prod { ... }
  }

  // Operations views — goes in operations-views.c4
  views 'Operations' {
    view ops_overview { ... }
  }
}
```

## When to stop

If a 1200-line file has no meaningful deployment or dynamic content, a 2-file split (`system-model.c4` + `system-views.c4`) is the correct target. Adding unused files creates premature structure.
