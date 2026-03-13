Relationship choice: model two explicit `reads`, not one smart composite relationship.
Short rule: Do not invent a kind such as `reads_with_fallback`. Keep the model relationships explicit and put fallback behavior in the labels or, if timing matters, in `create-sequence-view`.
Minimal example:
api -[reads]-> redisCache 'Checks cache' {
  technology 'Redis'
}
api -[reads]-> primaryDatabase 'Fetches on cache miss' {
  technology 'PostgreSQL'
}
api -[writes]-> redisCache 'Refreshes cached value'
Counter-example / anti-pattern:
api -[reads_with_fallback]-> primaryDatabase
That hides two distinct dependencies behind an invented kind.
