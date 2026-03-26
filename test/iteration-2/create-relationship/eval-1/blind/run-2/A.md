# Eval 1 — Async upload flow: return relationship?

## 1. Relationship choice

**No return relationship** from `worker` back to `uploadService`.

## 2. Rule

`async` expresses fire-and-forget messaging. The producer does not wait for a response. In a queue/worker flow, the worker has no structural obligation to notify the producer — do not add a return arrow.

## 3. Minimal example

```likec4
uploadService -[async]-> jobQueue 'Publishes job' {
  technology 'AMQP'
}

worker -[async]-> jobQueue 'Consumes job' {
  technology 'AMQP'
}

worker -[writes]-> primaryDatabase 'Stores processing result' {
  technology 'PostgreSQL'
}
```

## 4. Anti-pattern

```likec4
// ❌ Wrong: fake return path from async worker to producer
worker -[calls]-> uploadService 'Send completion'
```

## 5. Handoff

If the callback, completion notification, or fallback timing matters, keep the model relationships as above and add a `create-sequence-view` dynamic view to document the temporal order.
