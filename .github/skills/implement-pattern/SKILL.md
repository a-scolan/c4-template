---
name: implement-pattern
description: Use when adding a common architecture pattern such as an external integration, queue/worker flow, caching layer, webhook callback, or standard web/API/data stack and you need a safe LikeC4 starting structure.
---

# Apply LikeC4 Common Patterns

## Goal

Give a safe starter structure quickly, then tell the user what to substitute with the exact kinds and names from the active workspace.

These are **starter scaffolds**, not copy-paste truth.

## When to Use

- external third-party integration
- async queue/worker processing
- cache in front of a source-of-truth store
- standard web/API/data stack
- notification or webhook patterns

## Preconditions

- if exact kinds are unclear, use `lookup-element-kinds`
- create or adjust the elements with `create-element`
- create typed arrows with `create-relationship`

## Default response shape

1. name the pattern
2. give one minimal scaffold
3. list the substitutions to make (`parent`, `exact kinds`, `names`, `tech`) 
4. hand off only if the user is moving to timing/views/deployment

## Quick pattern map

| Pattern | Minimal relationship shape |
|---|---|
| External integration | `api -[calls]-> externalService` |
| Async queue/worker | `api -[async]-> queue` + `worker -[async]-> queue` |
| Cache + source of truth | `api -[reads]-> cache` + `api -[reads]-> database` |
| Web/API/data stack | `webapp -[calls]-> api` + `api -[reads/writes]-> database` |
| Notification flow | `api -[async]-> queue` + `worker -[calls]-> provider` |

## Compact scaffolds

### External integration

```likec4
externalService = System_External 'Third-Party API' {
  technology 'HTTPS API'
  description 'External service used by the platform.'
}

api -[calls]-> externalService 'Processes request' {
  technology 'HTTPS'
}
```

### Async queue/worker

```likec4
queue = Container_Queue 'Job Queue' {
  technology 'RabbitMQ'
  description 'Buffers asynchronous work.'
}

api -[async]-> queue 'Publishes job' {
  technology 'AMQP'
}

worker -[async]-> queue 'Consumes job' {
  technology 'AMQP'
}
```

### Cache + source of truth

```likec4
cache = Container 'Redis Cache' {
  technology 'Redis'
  description 'Hot-data cache.'
}

api -[reads]-> cache 'Checks cache'
api -[reads]-> database 'Fetches on cache miss'
api -[writes]-> cache 'Refreshes cache'
api -[writes]-> database 'Persists source-of-truth changes'
```

Use a more specific declared cache/container kind if the workspace provides one.

### Web/API/data stack

```likec4
webapp = Container_Webapp 'Web App' {
  technology 'React'
  description 'User interface.'
}

api = Container_Api 'API' {
  technology 'Node.js'
  description 'Business logic.'
}

database = Container_Database 'Database' {
  technology 'PostgreSQL'
  description 'Canonical data store.'
}

webapp -[calls]-> api 'Sends API requests'
api -[reads]-> database 'Queries data'
api -[writes]-> database 'Persists changes'
```

### Notification flow

```likec4
notificationQueue = Container_Queue 'Notification Queue' {
  technology 'RabbitMQ'
  description 'Queues outbound notifications.'
}

notificationWorker = Container 'Notification Worker' {
  technology 'Worker runtime'
  description 'Delivers queued notifications.'
}

provider = System_External 'Notification Provider' {
  technology 'HTTPS API'
  description 'External delivery provider.'
}

api -[async]-> notificationQueue 'Publishes notification job' {
  technology 'AMQP'
}

notificationWorker -[async]-> notificationQueue 'Consumes notification job' {
  technology 'AMQP'
}

notificationWorker -[calls]-> provider 'Delivers notification' {
  technology 'HTTPS'
}
```

## Pattern rules that must survive every scaffold

- async flows are one-way; do not add return calls from workers
- reads/writes are for data access; databases are not generic service calls
- keep the database as source of truth when cache is present
- do not invent undeclared kinds or relationship types
- if callback/webhook order matters, move the temporal story to `create-sequence-view`

## If MCP is unavailable

Use the local shared specs and model files to choose the nearest declared kinds, then provide the scaffold immediately. List the exact substitutions to verify later when tooling is back.

## Handoffs

- exact kinds unclear → `lookup-element-kinds`
- element declarations need cleanup → `create-element`
- relationship details need tuning → `create-relationship`
- callbacks, retries, or webhook timing matter → `create-sequence-view`
