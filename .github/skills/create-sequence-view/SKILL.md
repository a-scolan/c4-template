---
name: create-sequence-view
description: Use when documenting a LikeC4 use case, temporal flow, or async behavior as a dynamic view, especially when order matters more than structure.
---

# Create Dynamic Sequence View

## Goal

Show **who starts the flow**, **what happens next**, and **in what order**.

Default answer shape:
1. confirm this belongs in `views 'Use Cases'`
2. provide one short dynamic-view scaffold
3. call out one critical anti-pattern if relevant

## When to Use

- user workflows
- async publish/consume flows
- validation or error paths
- webhook/callback ordering
- any case where temporal order matters more than static structure

**Do not use** for static C1/C2/C3/deployment views — use `design-view` for those.

## Hard rules

- start with the initiating actor or external trigger
- use plain `->` arrows only
- keep labels short and action-focused
- place dynamic views in `views 'Use Cases'`
- do not show parent → own-child interactions

## Minimal scaffold

```likec4
views 'Use Cases' {
  dynamic view uploadFlow {
    title 'Upload Flow'
    user -> webApp 'Opens upload form'
    webApp -> api 'POST /upload'
    api -> objectStorage 'Stores file'
    api -> jobQueue 'Queues processing'
    jobQueue -> worker 'Delivers job'
    worker -> primaryDatabase 'Updates metadata'
  }
}
```

## One anti-pattern to check first

```likec4
// ❌ Wrong in a dynamic view
user -> webApp
webApp -> webApp.authComponent
```

```likec4
// ✅ Better
user -> webApp.authComponent 'Starts login'
webApp.authComponent -> directoryService 'Validates credentials'
```

## If MCP is unavailable

You can still help:

1. infer the relevant actor, boundary, and step order from local model files
2. provide the shortest valid dynamic-view snippet
3. flag any element references that still need later confirmation

## Common mistakes

- ❌ missing initiating actor
- ❌ using `-[calls]->` instead of plain `->`
- ❌ placing the view outside `views 'Use Cases'`
- ❌ showing parent → own-child calls
- ❌ mixing static structure explanation into the sequence instead of showing temporal steps
