---
name: design-view
description: Use when creating or updating architecture views with proper element inclusion, parent context, neighbor relationships, and category folder organization (C1/C2/C3/Use Cases/Deployment/Operations).
---

# Design LikeC4 View

## Goal

Create a view that shows the **parent boundary**, the **focus**, and the **neighbors** — without over-constraining layout or redrawing the model.

Default answer shape:
1. choose the correct folder and view type
2. state the include strategy
3. provide one short scaffold
4. add layout/navigation notes only if needed

## When to Use

- Creating or updating C1/C2/C3, Deployment, or Operations views
- Deciding what to include around a focus element
- Organizing views into the correct category blocks
- Adding minimal layout hints after the basic scaffold is correct

**Do not use** for dynamic/sequence flows — use `create-sequence-view`.

## Hard rules

| Rule | What it means |
|---|---|
| Parent context is mandatory | show what contains the focus |
| Neighbors are mandatory for focused views | include incoming and outgoing interactions |
| Category folders are mandatory | every view except `view index` belongs in a named `views '...'` block |
| Deployment views use explicit includes | list environment, zones, clusters if any, and each VM explicitly |
| Logical app traffic stays in the model | deployment views inherit it via `instanceOf`; do not redraw it |
| Layout hints are last resort | start with no `rank` hints |

## Folder map

- `views { view index ... }` → root index only
- `views 'C1'` → static system context
- `views 'C2'` → container views
- `views 'C3'` → component views
- `views 'Use Cases'` → dynamic views (handled by `create-sequence-view`)
- `views 'Deployment'` → infrastructure topology
- `views 'Operations'` → security/monitoring/DR/CI-CD operational views

## Default include strategy

### C2 / C3 focused static views

```likec4
views 'C3' {
  view c3_uploadService {
    title 'Upload Service'
    include corePlatform.uploadService
    include corePlatform.uploadService.*
    include -> corePlatform.uploadService
    include corePlatform.uploadService ->
  }
}
```

Use the same idea for C2, but with the parent **system** instead of the parent container.

### C1 context scaffold

```likec4
views 'C1' {
  view c1_context {
    title 'System Context'
    include customer
    include corePlatform
    include externalPaymentGateway
  }
}
```

### Deployment scaffold

```likec4
views 'Deployment' {
  deployment view overview {
    title 'Production Infrastructure'
    include production
    include production.dmzTier
    include production.appTier
    include production.dataTier
    include production.dmzTier.webVm
    include production.appTier.apiVm
    include production.appTier.workerVm
    include production.dataTier.dbVm
  }
}
```

## Deployment-specific rules

- include the environment first
- include each zone explicitly
- include each cluster explicitly if clusters are part of the hierarchy
- include **every VM explicitly**
- stop at VM by default; include `Node_App` only when showing placement or a real infra-specific exception
- never use deployment wildcards such as `production.*` or `production.**` for production-grade views

### Good vs bad deployment includes

```likec4
// ✅ Good
include production
include production.appTier
include production.appTier.apiVm
include production.dataTier.dbVm
```

```likec4
// ❌ Too vague
include production.*

// ❌ Too deep for a normal topology view
include production.appTier.apiVm.apiApp
```

## Layout guidance

Start with no `rank` hints.

Add layout control only when the preview is still hard to read:

```likec4
autoLayout TopBottom
rank source { user }
```

Rules of thumb:
- one obvious anchor is usually enough
- `autoLayout LeftRight` is optional, not a default
- if you want many `rank` hints, the include scope is probably wrong

## Navigation guidance

When you create a new detail view, wire the parent overview to it:

```likec4
include corePlatform.api with {
  navigateTo c3_api
}
```

## If MCP is unavailable

Still provide a useful scaffold:

1. infer the view boundary from the nearby model and view files
2. state the parent + focus + neighbor strategy
3. provide the shortest valid scaffold
4. list follow-up checks for later (`open-view`, parent boundary confirmation, include cleanup)

## Common mistakes

- ❌ missing parent boundary
- ❌ omitting neighbors on a focused view
- ❌ putting dynamic flows in `C1`/`C2`/`C3` instead of `Use Cases`
- ❌ using wildcards in deployment views
- ❌ redrawing app traffic in deployment views instead of relying on inherited logical relationships
- ❌ using many `rank` hints before fixing the include set

## More examples

Use [PATTERNS.md](PATTERNS.md) for longer worked examples and more specialized layouts.
