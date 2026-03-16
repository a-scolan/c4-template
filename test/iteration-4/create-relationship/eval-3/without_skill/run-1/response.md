Use two reads relationships, not one 'smart' relationship. The cache and the database are two distinct dependencies, so the model should show both:
api -[reads]-> redis 'Checks cache'
api -[reads]-> postgres 'Falls back on cache miss' {
  technology 'PostgreSQL'
}
If the API repopulates Redis after a miss, add a separate writes relationship to Redis.
