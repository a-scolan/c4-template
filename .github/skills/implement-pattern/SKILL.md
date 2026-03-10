---
name: implement-pattern
description: Use when implementing standard architectural patterns (async/queue workflows, external integrations, caching layers, multi-tier systems). Provides proven templates with clear responsibilities.
---

# Apply LikeC4 Common Patterns

Use this skill when implementing standard architectural patterns.

**Keywords:** queue, async, pattern, integration, caching, multi-tier, worker, message queue, external API, template

**Prerequisites:** Use `create-element` for proper kinds/tags and `create-relationship` for typed relationships.

## Pattern: External System Integration

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

## Pattern: Async Processing

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
