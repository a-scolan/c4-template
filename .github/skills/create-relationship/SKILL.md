---
name: create-relationship
description: Use when connecting LikeC4 elements and you need to choose the exact logical or deployment relationship kind, place technology in the right field, or decide whether a connection belongs in the model or only in deployment.
---

# Create LikeC4 Relationship

## Goal

Choose the exact relationship, explain the rule briefly, and show a paste-ready example.

Default answer shape:
1. **relationship choice**
2. **short rule**
3. **minimal example**
4. **counter-example / anti-pattern**
5. **handoff to `create-sequence-view`** only if timing or fallback order matters

## When to Use

- Connecting two existing elements in the logical model
- Choosing between `calls`, `async`, `reads`, `writes`, or `uses`
- Deciding whether the connection belongs in `model {}` or deployment
- Placing protocol or medium details such as `Manual`, `HTTPS`, `HTTP/8080`, `AMQP`, or `LDAP`
- Modeling queue/event flows without inventing return paths

**Do not use** to create the elements themselves — use `create-element` first.

## Local taxonomy to respect in this repository

### Model relationship kinds

`uses`, `calls`, `async`, `reads`, `writes`

### Deployment relationship kinds

`http`, `https`, `tcp`, `nfs`, `amqp`, `oidc_saml`, `ldap`, `sql`, `redis`, `smtp`

Normal application traffic belongs in the **system model** with a model relationship kind plus `technology '...'`. Deployment relationships are reserved for infrastructure-only exceptions.

## Quick decision table

| Need | Use | Avoid |
|---|---|---|
| Service invokes service | `-[calls]->` | inventing `invokes` |
| Read from cache/database/directory | `-[reads]->` | `-[calls]->` to data stores |
| Persist or mutate data | `-[writes]->` | generic `calls` for persistence |
| Queue/event flow | `-[async]->` | return arrows to the producer |
| Human interaction | `-[calls]->` + `technology 'Manual'` | deployment-only browser traffic |
| Protocol detail | `technology 'HTTPS'`, `technology 'HTTP/8080'`, `technology 'AMQP'` | putting protocol into model relationship kind |

## Teach by contrast

### Service-to-service request

```likec4
webApp -[calls]-> api 'Sends request' {
  technology 'HTTPS'
}
```

```likec4
// ❌ Wrong: kind in block
webApp -> api {
  calls 'Sends request'
  technology 'HTTPS'
}
```

### Reads vs calls

Use `calls` for service behavior, `reads` for data access.

```likec4
retrievalService -[reads]-> redisCache 'Checks cache'
retrievalService -[reads]-> primaryDatabase 'Fetches on cache miss'
```

```likec4
// ❌ Wrong: databases modeled as generic service calls
retrievalService -[calls]-> primaryDatabase 'Fetch data'
```

### Writes for persistence

```likec4
worker -[writes]-> primaryDatabase 'Stores processing result' {
  technology 'PostgreSQL'
}
```

### Async queue/worker flow

```likec4
uploadService -[async]-> jobQueue 'Publishes job' {
  technology 'AMQP'
}

worker -[async]-> jobQueue 'Consumes job' {
  technology 'AMQP'
}

worker -[writes]-> primaryDatabase 'Stores result' {
  technology 'PostgreSQL'
}
```

```likec4
// ❌ Wrong: fake return path from async worker to producer
worker -[calls]-> uploadService 'Send completion'
```

### Cache fallback is two reads, not a smart composite kind

```likec4
api -[reads]-> redisCache 'Checks cache'
api -[reads]-> primaryDatabase 'Fetches on cache miss'
api -[writes]-> redisCache 'Refreshes cached value'
```

```likec4
// ❌ Wrong: invented behavior-specific kind
api -[reads_with_fallback]-> primaryDatabase
```

If fallback timing or retries matter, keep the model relationships explicit and move the temporal story to `create-sequence-view`.

## Model first, deployment rarely

Prefer this:

```likec4
user -[calls]-> webApp 'Uses UI' {
  technology 'Manual'
}

webApp -[calls]-> api 'Sends request' {
  technology 'HTTPS'
}

api -[calls]-> internalService 'Routes request' {
  technology 'HTTP/8080'
}
```

Not this:

```likec4
// ❌ Duplicating normal app traffic in deployment
Prod.Web.webApp -[https]-> Prod.App.apiApp 'Browser traffic'
```

Use a deployment relationship only when the logical model does **not** already express the fact: monitoring scrapes, replication, bastion access, storage mounts, or an operational network hop.

## Relationship documentation standard

Always think in this order:

1. **Kind** — `calls`, `async`, `reads`, `writes`, `uses`
2. **Label** — short action phrase such as `Queues job`, `Fetches records`, `Authenticates user`
3. **Technology** — protocol or medium only (`Manual`, `HTTPS`, `HTTP/8080`, `AMQP`, `LDAP`, `SMTP`, `PostgreSQL`)
4. **Description** — optional, only when the label is still ambiguous

## If MCP is unavailable

Stay specific:

1. inspect `projects/shared/SPEC_CHEATSHEET.md` and `projects/shared/spec-*.c4`
2. verify whether you are in logical model vs deployment files
3. answer with the rule and the minimal example immediately
4. list the follow-up checks to run later (`find-relationships`, `read-project-summary`, preview affected views)

Do not fall back to generic “it depends” wording when the repository taxonomy already tells you the right relationship family.

## Common mistakes

```likec4
❌ api -> service 'Call endpoint'                 // Missing relationship kind
❌ api -> service { calls 'Call endpoint' }       // Kind in block
❌ api -[invokes]-> service                       // Invalid undeclared kind
❌ api -[reads_with_fallback]-> database          // Composite kind invented for behavior
❌ worker -[calls]-> uploadService 'Send completion'  // Fake return path in async flow
❌ Prod.Web.webApp -[https]-> Prod.App.apiApp     // Duplicated normal app traffic in deployment
```

## Handoffs

- Need the endpoints first? Use `create-element`
- Need the exact kinds available in the workspace? Use `lookup-element-kinds`
- Need retries, callbacks, fallback order, or webhook timing? Use `create-sequence-view`
