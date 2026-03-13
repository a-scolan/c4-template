No. Model the actual async chain, not an implied return path:
uploadService -[async]-> jobQueue 'Publishes job' {
  technology 'AMQP'
}
jobQueue -[async]-> worker 'Delivers job' {
  technology 'AMQP'
}
worker -[writes]-> database 'Stores upload metadata' {
  technology 'PostgreSQL'
}
Add a relationship back to `uploadService` only if the worker really calls back, sends a status update, or publishes an event that `uploadService` consumes.
