---
name: implement-pattern
description: Use when implementing standard architectural patterns (async/queue workflows, external integrations, caching layers, multi-tier systems). Provides proven templates with clear responsibilities.
---

# Apply LikeC4 Common Patterns

## Overview

Provides ready-to-use templates for recurring architectural patterns: external system integration, async queue/worker workflows, caching layers, multi-tier web architectures, and event notification pipelines. Each template shows the required elements and relationship kinds.

## When to Use

- Adding an integration with an external third-party API
- Modelling async background processing (queue + worker)
- Adding a caching layer in front of a database
- Defining a standard web + API + database stack
- Modelling event-driven notifications (email, webhooks)

**Prerequisites:** Use `create-element` for proper kinds/tags and `create-relationship` for typed relationships.

## Quick Reference

| Pattern | Key relationships |
|---------|------------------|
| External Integration | `api -[calls]-> externalService` |
| Async Queue/Worker | `api -[async]-> queue` + `worker -[async]-> queue` |
| Caching Layer | `api -[reads]-> cache` + `api -[reads]-> database` (miss) |
| Multi-Tier | `webapp -[calls]-> api -[reads/writes]-> database` |
| Event Notification | `api -[async]-> queue` + `notifier -[sends]-> external` |

## Pattern: External System Integration

```likec4
externalService = System_External 'Third-Party API' {
  technology 'REST API'
  description 'External payment processor'
  #External
}

mySystem.api -[calls]-> externalService 'Process payment'
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

api -[async]-> queue 'Publishes jobs'
worker -[async]-> queue 'Consumes jobs'
```

**Notes:**
- Async flows are one-way; do not add return calls from workers.
- Use `-[writes]->` for persistence and `-[reads]->` for queries.

## Pattern: Caching Layer

```likec4
cache = Container_Cache 'Cache' {
  technology 'Redis'
  description 'Low-latency cache for hot data'
}

api -[reads]-> cache 'Read-through cache'
api -[writes]-> cache 'Cache updates'
api -[reads]-> database 'Fetch on cache miss'
```

**Notes:**
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
notifier = Container_Service 'Notification Service' {
  technology 'Email/SMS Provider'
  description 'Delivers user notifications'
}

api -[async]-> queue 'Publish notification event'
notifier -[async]-> queue 'Consume notification event'
notifier -[sends]-> externalService 'Send notification'
```

**Notes:**
- Use `-[sends]->` for email/webhook delivery.
- Avoid synchronous calls for background notifications.

## Common Mistakes

❌ **Return relationship from worker** — async flows are one-way; never add `worker -[calls]-> api` or any return path

❌ **Using `-[calls]->` for database access** — use `-[reads]->` for queries and `-[writes]->` for mutations; database access is not a “call”

❌ **Missing `#External` tag** — all third-party systems must be tagged so they visually distinguish from internal elements

❌ **Cache as only source of truth** — always keep the database as authoritative source; cache is a read-through layer, not primary storage
