---
name: create-sequence-view
description: Use when documenting a LikeC4 use case, temporal flow, or async behavior as a dynamic view, especially when order matters more than structure.
---

# Create Dynamic Sequence View

## Overview

Dynamic (sequence) views show HOW the system behaves during important operations: who initiates, what happens, in what order. They use plain `->` arrows (no relationship kinds), always start with the triggering actor, and are grouped in the `'Use Cases'` view folder.

## When to Use

- Documenting a user workflow (upload, login, checkout)
- Showing async patterns (queue publish → consume → persist)
- Clarifying error flows, validation paths, or recovery procedures
- Any scenario where temporal order and causality need to be explicit

**Do not use** for structural diagrams (C1/C2/C3 static views) — use `design-view` for those. Dynamic views cannot show parent → own-child relationships.

## Quick Reference

- Start with the initiating actor.
- Use plain arrows (`->`), no relationship kinds.
- Keep labels action-focused and time-ordered.
- Place all dynamic views in `views 'Use Cases'`.
- Avoid parent → child calls inside the same container.

## Core Requirement: Always Include Initiating Actors

**Dynamic views MUST explicitly show the actor(s) that initiate the flow for context:**
- Start every sequence with the external actor (user, external system, scheduler)
- Show which user action triggers which internal flows
- Make causality explicit: "Who does what? When? Why?"
- This answers: "What triggers this behavior? Who is involved?"

## Organization & Purpose

Place sequence/dynamic views in the `'Use Cases'` subfolder to show **temporal flows** - how the system behaves during important operations.

**Types of use cases to document:**
- **User workflows:** Upload → validation → processing → storage (happy path)
- **Validation & error flows:** Input validation, exception handling, retries
- **Async patterns:** Message queues, background jobs, notifications
- **Data flows:** Data movement through system (retrieval, transformation, storage)
- **Disaster recovery:** Failover, replication, recovery procedures
- **Integration patterns:** External system interactions, polling, webhooks

```likec4
views 'Use Cases' {
  dynamic view upload_flow { ... }
  dynamic view retrieval_flow { ... }
  dynamic view backup_replication { ... }
  dynamic view error_handling { ... }
}
```

## Requirements

1. **Use `dynamic view`** with descriptive ID
2. **Include initiating actor** - ALWAYS start with external actor (user, system, scheduler)
3. **No relationship kinds:** Use plain `->` not `-[kind]->`
4. **Step labels:** Add descriptive text for each interaction explaining WHAT happens
5. **Temporal order:** Steps execute top-to-bottom showing sequence
6. **Folder organization:** Group all use cases in `views 'Use Cases'` subfolder
7. **Title format:** "[WorkflowName]" (e.g., "Upload") — the folder already provides the category
8. **CRITICAL: No parent-child relationships** - Cannot show `container -> container.component`

## Parent-Child Restriction

**Dynamic views CANNOT show a parent element calling its own child:**

```likec4
// ❌ INVALID: Container calling its own component
user -> webApp
webApp -> webApp.authComponent   // ❌ COMPILATION ERROR!

// ✅ CORRECT: Actor directly accesses component
user -> authComponent 'Initiates login'
authComponent -> directoryService 'Validates credentials'
```

**Why this restriction exists:**
- Dynamic views show interactions BETWEEN independent parts
- Parent-child is a containment relationship, not an interaction
- In real systems, actors interact with specific components, not abstract containers

## Example

```likec4
views 'Use Cases' {
  dynamic view sequence_upload {
    title 'Document Upload Flow'
    
    user -> webApp 'Opens upload form'
    webApp -> api 'POST /upload'
    api -> objectStorage 'Store file'
    api -> jobQueue 'Queue processing job'
    jobQueue -> worker 'Execute job'
    worker -> primaryDatabase 'Update metadata'
  }
}
```

## Common Mistakes

❌ **Omitting the initiating actor** — every sequence MUST start with the external actor (user, system, scheduler)

❌ **Using `-[calls]->`** — dynamic views MUST use plain `->` only; relationship kinds cause compilation errors

❌ **Placing views outside `'Use Cases'`** — all dynamic views belong in the `views 'Use Cases'` folder

❌ **Parent calling its own child** (`container -> container.component`) — dynamic views cannot show containment; have the actor address the component directly

❌ **Steps out of temporal order** — each arrow must represent the next real action in time; avoid circular or back-and-forth patterns
