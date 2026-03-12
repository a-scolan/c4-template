---
name: implement-pattern
description: Use when adding a common architecture pattern such as an external integration, queue/worker flow, caching layer, webhook callback, or standard web/API/data stack and you need a safe LikeC4 starting structure.
---

# Apply LikeC4 Common Patterns

## Overview

Provides starter patterns for recurring architectural structures: external integrations, async queue/worker workflows, caching layers, multi-tier request paths, and outbound/inbound notification flows.

These patterns are **starting structures**, not copy-paste truth. Always use kinds and relationship types that are actually declared in the active workspace.

## When to Use

- Adding an integration with an external third-party API
- Modelling async background processing (queue + worker)
- Adding a caching layer in front of a database
- Defining a standard web + API + database stack
- Modelling event-driven notifications (email, webhooks)

**Prerequisites:**
- Use `lookup-element-kinds` if you are unsure which exact kinds exist in the active workspace
- Use `create-element` for element creation
- Use `create-relationship` for typed relationships

## Quick Reference

| Pattern | Key relationships |
|---------|------------------|
| External Integration | `api -[calls]-> externalService` |
| Async Queue/Worker | `api -[async]-> queue` + `worker -[async]-> queue` |
| Caching Layer | `api -[reads]-> cache` + `api -[reads]-> database` (miss) |
| Multi-Tier | `webapp -[calls]-> api -[reads/writes]-> database` |
| Event Notification | `api -[async]-> queue` + `worker -[calls]-> externalProvider` |

## Pattern: External System Integration

```likec4
externalService = System_External 'Third-Party API' {
  technology 'REST API'
  description 'External payment processor'
  #External
}

api -[calls]-> externalService 'Process payment' {
  technology 'HTTPS'
}
```

**Notes:**
- Tag externals with `#External` (or the shared spec external tag).
- Keep the relationship label action-focused (e.g., “Process payment”).

## Pattern: Async Processing (Queue + Worker)

```likec4
queue = Container_Queue 'Job Queue' {
  technology 'RabbitMQ'
  description 'Async job processing'
}

api -[async]-> queue 'Publishes job' {
  technology 'AMQP'
}

worker -[async]-> queue 'Consumes job' {
  technology 'AMQP'
}
```

**Notes:**
- Async flows are one-way; do not add return calls from workers.
- Use `-[writes]->` for persistence and `-[reads]->` for queries.

## Pattern: Caching Layer

```likec4
cache = Container 'Redis Cache' {
  technology 'Redis'
  description 'Low-latency cache for hot data'
}

api -[reads]-> cache 'Read-through cache'
api -[writes]-> cache 'Cache updates'
api -[reads]-> database 'Fetch on cache miss'
api -[writes]-> database 'Persist source-of-truth changes'
```

**Notes:**
- Use a declared cache-specific kind if the active workspace has one. Otherwise, use a valid declared generic/container kind and make the cache role clear in title + technology.
- Use cache for hot reads; keep the database as source of truth.
- Use `reads`/`writes` for data access.

## Pattern: Multi-Tier Architecture

```likec4
webapp = Container_Webapp 'Web App' {
  technology 'React'
  description 'User interface'
}

api = Container_Api 'API' {
  technology 'Node.js'
  description 'Business logic'
}

database = Container_Database 'Database' {
  technology 'PostgreSQL'
  description 'Data persistence'
}

webapp -[calls]-> api 'API requests'
api -[reads]-> database 'Queries'
api -[writes]-> database 'Updates'
```

## Pattern: Event Notification

```likec4
notificationQueue = Container_Queue 'Notification Queue' {
  technology 'RabbitMQ'
}

notificationWorker = Container 'Notification Worker' {
  technology 'Worker runtime'
  description 'Consumes notification jobs'
}

externalProvider = System_External 'Notification Provider' {
  technology 'Email API'
  #External
}

api -[async]-> notificationQueue 'Publish notification job' {
  technology 'AMQP'
}

notificationWorker -[async]-> notificationQueue 'Consume notification job' {
  technology 'AMQP'
}

notificationWorker -[calls]-> externalProvider 'Deliver notification' {
  technology 'HTTPS'
}
```

**Notes:**
- Model the outbound delivery as an explicit second interaction, not as a return path from the first call.
- Use `create-sequence-view` if webhook or callback order matters.

## Common Mistakes

❌ **Return relationship from worker** — async flows are one-way; never add `worker -[calls]-> api` or any return path

❌ **Using `-[calls]->` for database access** — use `-[reads]->` for queries and `-[writes]->` for mutations; database access is not a “call”

❌ **Missing `#External` tag** — all third-party systems must be tagged so they visually distinguish from internal elements

❌ **Inventing undeclared kinds or relationship types** — if the workspace has no `Container_Cache` or `sends`, do not invent them; choose a valid declared kind and model the interaction explicitly

❌ **Cache as only source of truth** — always keep the database as authoritative source; cache is a read-through layer, not primary storage

## Handoffs

- Need the exact kinds available in this workspace? Use `lookup-element-kinds`
- Need to create the elements cleanly? Use `create-element`
- Need exact relationship syntax or technology placement? Use `create-relationship`
- Need temporal ordering for webhooks, retries, or callbacks? Use `create-sequence-view`
