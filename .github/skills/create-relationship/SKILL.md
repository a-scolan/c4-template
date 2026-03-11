---
name: create-relationship
description: Use when connecting elements in model or deployment files with typed relationships (calls, async, reads, writes), proper FQN usage, and descriptive labels.
---

# Create LikeC4 Relationship

## Overview

Defines how to declare typed directional relationships between LikeC4 elements. Relationship kind goes in the arrow (`-[kind]->`), never in the property block. Labels are action-focused, technology is protocol-only, and there are no return relationships.

## When to Use

- Connecting two elements in a system model or deployment file
- Choosing between `calls`, `async`, `reads`, `writes`, or `uses`
- Documenting async queue/event flows (no return paths)
- Adding protocol and technology details to a relationship

**Do not use** for creating elements themselves — see `create-element`. For sequence views, use `create-sequence-view` (plain `->` arrows, no kinds).

**REQUIRED BACKGROUND:** Read `create-element` skill and understand element kinds before creating relationships.

## Quick Reference

- Put the relationship kind in the arrow (never in the properties block).
- Use one-way async relationships for queues/events (no return relationships).
- Use `reads`/`writes` for data access; reserve `calls` for service-to-service requests.

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
3. **Technology** (in properties) - Protocol only: "HTTPS", "SSH", "LDAP". Add port only for non-default: "HTTP/8080"
4. **Description** (optional) - Only if label doesn't fully explain the interaction

**NEVER use descriptions for clarification if a better label works.** Keep technology field to protocol only, add port after "/" only for non-default ports.

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

// Write operation (persistence, not call)
worker -[writes]-> database 'Persist results' {
  technology 'PostgreSQL'
}

// Minimal syntax (when tech is obvious)
api -[calls]-> service 'Call endpoint'
cache -[reads]-> config 'Load settings'
```

**Best Practice:** Use protocol only for technology (e.g., "HTTPS", "SSH", "AMQP"), add port after "/" only for non-default ports (e.g., "HTTP/8080"). Keep labels short and action-focused. Descriptions in properties block are optional if the label is already clear.

## Common Mistakes

```likec4
❌ api -> service 'Calls'                     // Missing relationship kind
❌ api -> service { calls 'Action' }          // Type in block (INVALID!)
❌ mySystem.api -[invokes]-> service          // Invalid relationship kind
❌ client -[calls]-> server 'Request'
   server -[calls]-> client 'Response'       // No return relationships!
```
