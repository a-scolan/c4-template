---
name: create-relationship
description: Use when connecting LikeC4 elements and you need to choose the exact logical or deployment relationship kind, place technology in the right field, or decide whether a connection belongs in the model or only in deployment.
---

# Create LikeC4 Relationship

## Overview

Declare typed directional relationships between LikeC4 elements without blurring three separate concerns:
- **kind** goes in the arrow (`-[calls]->`, `-[reads]->`, `-[async]->`)
- **label** stays inline and action-focused
- **technology** describes the interaction medium or protocol

**Default rule:** model normal application traffic in the **system model** and let deployment instances inherit it via `instanceOf`. Deployment relationships are rare infrastructure-only exceptions.

## When to Use

- Connecting two elements in the logical model
- Choosing between `calls`, `async`, `reads`, `writes`, or `uses`
- Deciding whether a connection belongs in the model or only in deployment
- Adding protocol or medium details such as `Manual`, `HTTPS`, `HTTP/8080`, `AMQP`, or `LDAP`
- Modeling queue/event flows without inventing return paths

**Do not use** for creating elements themselves — use `create-element` first. For temporal order, retries, fallback logic, or webhook sequencing, use `create-sequence-view`.

## Quick Reference

| Need | Preferred pattern | Avoid |
|------|-------------------|-------|
| Service-to-service request | `source -[calls]-> target` | inventing a custom kind like `invokes` |
| Data retrieval | `service -[reads]-> store` | `service -[calls]-> database` |
| Data mutation | `service -[writes]-> store` | modeling persistence as a generic call |
| Queue/event flow | `producer -[async]-> queue`, `worker -[async]-> queue` | return relationships back to the producer |
| Human interaction | `user -[calls]-> ui { technology 'Manual' }` | treating human actions as deployment traffic |
| Protocol detail | `technology 'HTTPS'` or `technology 'HTTP/8080'` | putting protocol in the relationship kind for normal app traffic |

## Model First, Deployment Rarely

Model the relationship once in `model {}` and let deployment instances inherit it.

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

api -[reads]-> primaryDatabase 'Reads records' {
  technology 'PostgreSQL'
}

webAppInstance = Node_App 'Web App' {
  instanceOf webApp
}

apiInstance = Node_App 'API' {
  instanceOf api
}
```

```likec4
// ❌ Anti-pattern: repeating app traffic in deployment just to show protocol/port
Prod.Web.webApp -[https]-> Prod.App.apiApp 'Browser traffic'
Prod.App.apiApp -[tcp]-> Prod.Data.database 'Reads records'
```

Add a deployment relationship only when it documents an infrastructure fact that the logical model does not express: replication, monitoring scrapes, bastion access, or a network hop that matters operationally.

## Relationship Syntax

**The relationship kind goes in the arrow, never in the properties block.**

```likec4
// ✅ Correct
source -[calls]-> target 'Action description' {
  technology 'HTTPS'
}

// ✅ Also correct when technology is obvious
service -[reads]-> database 'Query records'

// ❌ Wrong: kind in the block
source -> target {
  calls 'Action description'
  technology 'HTTPS'
}

// ❌ Wrong: missing kind
source -> target 'Action description'
```

## Async & Event-Driven Flows

Use `-[async]->` for queue and event flows. Async is one-way: do **not** model an ACK or result as a return relationship to the producer.

```likec4
uploadApi -[async]-> jobQueue 'Publishes job' {
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
// ❌ Wrong: fake synchronous return path
worker -[calls]-> uploadApi 'Send completion'
```

If the timing matters — validation before queuing, fallback behavior, webhook callback order — keep the model relationships explicit and move the temporal story to `create-sequence-view`.

## Reads, Writes, and Fallback Logic

Use `reads` and `writes` for data access. Do not invent composite kinds such as `reads_with_fallback`.

```likec4
api -[reads]-> cache 'Check cache'
api -[reads]-> primaryDatabase 'Fetch on cache miss'
api -[writes]-> cache 'Refresh cached value'
```

If you need to explain fallback, put it in the label or in a dynamic view — not in a custom relationship kind.

## Relationship Documentation Standard

Always think in this order:
1. **Kind** — `calls`, `async`, `reads`, `writes`, `uses`
2. **Label** — short action phrase such as `Queues job`, `Fetches records`, `Authenticates user`
3. **Technology** — protocol or medium only, such as `Manual`, `HTTPS`, `HTTP/8080`, `AMQP`, `LDAP`, `SMTP`, `PostgreSQL`
4. **Description** — optional, only when the label still leaves an important ambiguity

### Common Technology Values

| Situation | Technology value |
|---|---|
| Human interaction | `Manual` |
| TLS browser or service call | `HTTPS` |
| Non-default internal HTTP | `HTTP/8080` |
| Queue/event broker | `AMQP` |
| PostgreSQL access | `PostgreSQL` |
| Generic SQL access | `SQL` |
| Directory lookup | `LDAP` |
| Mail delivery | `SMTP` |
| Federation / SSO | `OIDC/SAML` |

## Common Mistakes

```likec4
❌ api -> service 'Call endpoint'                 // Missing relationship kind
❌ api -> service { calls 'Call endpoint' }       // Kind in block
❌ api -[invokes]-> service                       // Invalid undeclared kind
❌ api -[reads_with_fallback]-> database          // Composite kind invented for behavior
❌ worker -[calls]-> uploadApi 'Send completion'  // Fake return path in async flow
❌ Prod.Web.webApp -[https]-> Prod.App.apiApp     // Duplicated app traffic in deployment
```

## Handoffs

- Need exact kinds for the endpoints? Use `lookup-element-kinds`
- Need to create the endpoints first? Use `create-element`
- Need to show retries, fallback, or webhook timing? Use `create-sequence-view`
