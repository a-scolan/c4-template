Relationship choice: `async` for the queue flow, then `writes` for persistence.
Rule: Model the async flow explicitly and do not invent a fake return path to the producer unless there is a real callback or notification.
Example:
uploadService -[async]-> jobQueue 'Publishes job' {
  technology 'AMQP'
}
worker -[async]-> jobQueue 'Consumes job' {
  technology 'AMQP'
}
worker -[writes]-> primaryDatabase 'Stores result' {
  technology 'PostgreSQL'
}
Anti-pattern:
worker -[calls]-> uploadService 'Send completion'
Handoff: If completion timing, retries, or callback order matter, move that story to `create-sequence-view`.
