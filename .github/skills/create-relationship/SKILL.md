---
name: create-relationship
description: Use when connecting LikeC4 elements and choosing relationship kinds or technology values, especially in system model files where deployment models and views should inherit those relationships instead of restating them.
---

# Create LikeC4 Relationship

## Overview

Defines how to declare typed directional relationships between LikeC4 elements. Relationship kind goes in the arrow (`-[kind]->`), never in the property block. Labels are action-focused, technology is the communication medium or protocol, and there are no return relationships.

**Default rule:** put application relationships in the **system model** and let deployment models/views inherit them via `instanceOf`. Deployment relationships are rare exceptions for infrastructure-only hops.

## When to Use

- Connecting two elements in a system model
- Choosing the technology value to attach to a logical relationship (`Manual`, `HTTPS`, `HTTP/8080`, `AMQP`, `LDAP`, etc.)
- Deciding whether a relationship belongs in the logical model or is one of the rare infrastructure-only deployment edges
- Choosing between `calls`, `async`, `reads`, `writes`, or `uses`
- Documenting async queue/event flows (no return paths)
- Adding protocol and technology details to a relationship

**Do not use** for creating elements themselves — see `create-element`. For sequence views, use `create-sequence-view` (plain `->` arrows, no kinds). Do not use this skill to redraw app-level traffic in deployment models or deployment views; those relationships should come from the system model.

**REQUIRED BACKGROUND:** Read `create-element` skill and understand element kinds before creating relationships.

## Quick Reference

- Put the relationship kind in the arrow (never in the properties block).
- Prefer the logical system model over deployment for application relationships.
- Put communication technology on the logical relationship; use `Manual` for human interaction.
- Add a port only when it is non-default for the protocol (for example `HTTP/8080`).
- Use one-way async relationships for queues/events (no return relationships).
- Use `reads`/`writes` for data access; reserve `calls` for service-to-service requests.

## Model First, Deployment Rarely

Model the relationship once in `model {}` and let deployment instances inherit it.

```likec4
// ✅ Preferred: logical relationship carries the action and technology
user -[calls]-> mySystem.webapp 'Uses UI' {
  technology 'Manual'
}

mySystem.webapp -[calls]-> mySystem.api 'Makes API requests' {
  technology 'HTTPS'
}

mySystem.api -[calls]-> internalBackend 'Routes uploads' {
  technology 'HTTP/8080'
}

mySystem.api -[reads]-> mySystem.database 'Queries metadata' {
  technology 'PostgreSQL'
}

// deployment.c4
webApp = Node_App 'Web Application' {
  instanceOf mySystem.webapp
}

apiApp = Node_App 'API Server' {
  instanceOf mySystem.api
}

dbApp = Node_App 'Database' {
  instanceOf mySystem.database
}
```

```likec4
// ❌ Anti-pattern: repeating logical traffic in deployment just to show protocol/port
Prod.WebTier.WebVm.webApp -[https]-> Prod.AppTier.ApiVm.apiApp 'Makes API requests'
Prod.AppTier.ApiVm.apiApp -[tcp]-> Prod.DataTier.DbVm.dbApp 'Queries metadata'
```

Only add a deployment relationship when it documents an infrastructure fact that is not already expressed by the logical model: monitoring scrape paths, backup replication, bastion/SSH access, or a VM-to-VM/network-segment hop that matters operationally.

## Async & Event-Driven Patterns

### The Async Relationship Kind

Use `-[async]->` for message queue and event-driven flows. This creates **no return path** — workers never call back to the publisher.

```likec4
// ✅ Correct: Upload service queues a job, worker consumes it
uploadService -[async]-> jobQueue 'Queue file for processing'
jobQueue -[async]-> worker 'Deliver job'

// ❌ Wrong: Do NOT create call relationships FROM/TO workers
worker -[calls]-> uploadService   // ANTI-PATTERN!
uploadService -[calls]-> worker   // ANTI-PATTERN!
```

### Fail-Fast Pattern with Sync Validation

Validation happens **synchronously** in the producer service BEFORE queuing:

```likec4
model {
  vault = System {
    // Upload service validates FIRST (synchronous)
    uploadService = Container_Service 'Upload Service' {
      validateModule = Component 'Validate' { ... }
      queueModule = Component 'Queue Publisher' { ... }
    }
    
    jobs = Container_Queue 'Job Queue' { ... }
    
    worker = Container_Service 'Worker' {
      // Worker ONLY consumes and processes
      consumerModule = Component 'Consumer' { ... }
    }
  }
  
  // Flow: Validation (sync) → Queue (async) → Processing (async)
  vault.uploadService.validateModule -[uses]-> vault.uploadService.queueModule 'Publish if valid'
  vault.uploadService.queueModule -[async]-> vault.jobs 'Queue validated job'
  vault.worker.consumerModule -[async]-> vault.jobs 'Consume jobs'
}
```

### Relationship Kinds for Async

```likec4
// Async patterns (one-way, no return)
-[async]->       // Message queue, events, notifications
-[sends]->       // Email, alerts, webhooks
-[writes]->      // Database persist (not a call, just mutation)
-[reads]->       // Database query (not a call, just retrieval)

// Example upload → processing flow
uploadService -[async]-> jobQueue 'Queue file'     // ✅ One direction
jobQueue -[async]-> worker 'Deliver job'          // ✅ Message flow
worker -[writes]-> database 'Update status'       // ✅ Persistence, not call
worker -[writes]-> storage 'Save file'            // ✅ Persistence, not call
```

### Retrieval Flow Pattern

For services that fetch from storage/cache, use `-[reads]->` not `-[calls]->`:

```likec4
// ✅ Correct: Reading from database/cache
retrievalService -[reads]-> metadata 'Fetch document metadata'
retrievalService -[reads]-> cache 'Check cache for data'
retrievalService -[reads]-> storage 'Fetch encrypted file'

// ❌ Wrong: Database queries are not "calls"
retrievalService -[calls]-> metadata   // ANTI-PATTERN!
```

## Relationship Syntax (CRITICAL)

**The relationship kind MUST be in the arrow, NEVER in the property block:**

```likec4
// ✅ CORRECT: Type in arrow, label inline, properties in block
source -[calls]-> target 'Action description' {
  technology 'HTTPS'
}

// ✅ CORRECT: Type in arrow, minimal syntax
source -[reads]-> database 'Query data'

// ❌ WRONG: Type in block (compilation error!)
source -> target {
  calls 'Action description'    // ❌ INVALID!
  technology 'HTTPS'
}

// ❌ WRONG: Missing relationship kind
source -> target 'Action'       // ❌ Must specify type!
```

## Relationship Documentation Standard

Always document relationships with:
1. **Relationship Kind** (in arrow) - `calls`, `async`, `reads`, `writes`, `uses`
2. **Short Label** (inline) - Action-focused: "Fetches data", "Proxies requests", "Builds images"
3. **Technology** (in properties) - Communication medium or protocol only: `Manual`, `HTTPS`, `LDAP`, `AMQP`, `PostgreSQL`, `SMTP`. Add port only for non-default protocols: `HTTP/8080`
4. **Description** (optional) - Only if label doesn't fully explain the interaction

**NEVER use descriptions for clarification if a better label works.** Keep the technology field to the interaction medium/protocol, and add port after `/` only for non-default ports.

### Common Technology Values

| Situation | Technology value |
|---|---|
| Human uses UI or performs an operational step | `Manual` |
| Browser or service call over TLS | `HTTPS` |
| Internal HTTP on non-default port | `HTTP/8080` |
| Queue or event broker | `AMQP` |
| PostgreSQL access | `PostgreSQL` |
| Generic relational DB access | `SQL` |
| Directory lookup | `LDAP` |
| Mail delivery | `SMTP` |
| Federation / SSO | `OIDC/SAML` |
| Network file share | `NFS` |

```likec4
// ✅ Good: Clear label + protocol (default port)
api -[calls]-> service 'Fetches user data' {
  technology 'HTTPS'
}

// ✅ Good: Non-default port specified
proxy -[calls]-> backend 'Routes requests' {
  technology 'HTTP/8080'
}

// ✅ Good: Minimal (tech is obvious)
cache -[reads]-> config 'Load settings'

// ❌ Bad: Verbose technology field
api -[calls]-> service 'Fetches user data' {
  technology 'HTTPS REST API'   // Too verbose! Just "HTTPS"
}

// ❌ Bad: Redundant description
api -[calls]-> service 'Fetches data via HTTPS' {
  technology 'HTTPS'
  description 'OAuth 2.0 authentication with JWT tokens'   // Too much detail!
}
```

## Complete Examples

**Format:** `relationship kind` (in arrow) + `label` (inline) + `technology` (protocol only, port for non-default) in properties block. No need for descriptions if label is clear.

```likec4
// Human interaction
user -[calls]-> mySystem.webapp 'Uses UI' {
  technology 'Manual'
}

// Synchronous call with protocol (default port)
mySystem.api -[calls]-> externalService 'Fetches user data' {
  technology 'HTTPS'
}

// Non-default port
mySystem.api -[calls]-> backend 'Routes requests' {
  technology 'HTTP/8080'
}

// Database read
mySystem.service -[reads]-> mySystem.postgres 'Query records' {
  technology 'PostgreSQL'
}

// Async message (one-way, no response)
mySystem.publisher -[async]-> mySystem.queue 'Publish event' {
  technology 'AMQP'
}

// Container to external system
devforge.forgejoWeb -[calls]-> ldapServer 'Authenticate user' {
  technology 'LDAP'
}

// Email delivery
notificationService -[calls]-> mailServer 'Send notification' {
  technology 'SMTP'
}

// Write operation (persistence, not call)
worker -[writes]-> database 'Persist results' {
  technology 'PostgreSQL'
}

// Minimal syntax (when tech is obvious)
api -[calls]-> service 'Call endpoint'
cache -[reads]-> config 'Load settings'
```

**Best Practice:** Keep application protocols on system-model relationships so deployment diagrams can inherit them. Use concise technology values such as `Manual`, `HTTPS`, `AMQP`, `LDAP`, `SMTP`, `PostgreSQL`, or `OIDC/SAML`, and add port after `/` only for non-default ports (e.g., `HTTP/8080`). Keep labels short and action-focused. Descriptions in properties block are optional if the label is already clear.

## Common Mistakes

```likec4
❌ api -> service 'Calls'                     // Missing relationship kind
❌ api -> service { calls 'Action' }          // Type in block (INVALID!)
❌ mySystem.api -[invokes]-> service          // Invalid relationship kind
❌ client -[calls]-> server 'Request'
   server -[calls]-> client 'Response'       // No return relationships!
❌ Prod.Web.webApp -[https]-> Prod.App.apiApp 'UI traffic' // Duplicate deployment relationship
```
