Relationship choice: model it with two explicit `reads`, and usually one `writes` back to cache if the API refreshes it.
Rule: Do not invent one smart composite relationship for cache fallback. Keep the structural facts explicit in the model.
Example:
api -[reads]-> redisCache 'Checks cache'
api -[reads]-> primaryDatabase 'Fetches on cache miss'
api -[writes]-> redisCache 'Refreshes cached value'
Anti-pattern:
api -[reads_with_fallback]-> primaryDatabase
Handoff: If fallback timing, retries, or miss-handling order matter, capture that in `create-sequence-view`.
