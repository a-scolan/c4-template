Use two explicit `reads`, not one 'smart' relationship. Model the two real dependencies and keep the cache-miss logic in the labels or descriptions:
api -[reads]-> redis 'Checks cache' {
  technology 'Redis'
}
api -[reads]-> postgres 'Loads on cache miss' {
  technology 'PostgreSQL'
}
If the API repopulates Redis after a miss, add a separate `writes` relationship to Redis.
