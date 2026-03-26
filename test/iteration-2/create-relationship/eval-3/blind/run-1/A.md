# Eval 3 — Cache-then-fallback: one smart relationship or two `reads`?

## 1. Relationship choice

**Two explicit `reads`** (plus one `writes` if the cache is refreshed).

## 2. Rule

Model the actual data stores accessed with individual relationships. Do not invent composite or behavior-specific relationship kinds to encode business logic. Two `reads` are explicit, accurate, and queryable by tooling. If fallback timing or retry order matters, that is a concern for a sequence view — not the structural model.

## 3. Minimal example

```likec4
api -[reads]-> redisCache 'Checks cache'
api -[reads]-> primaryDatabase 'Fetches on cache miss'
api -[writes]-> redisCache 'Refreshes cached value'
```

## 4. Anti-pattern

```likec4
// ❌ Wrong: invented composite kind encodes behavior in the kind name
api -[reads_with_fallback]-> primaryDatabase

// ❌ Wrong: collapsing both data stores into one ambiguous relationship
api -[reads]-> redisCache 'Cache or DB'
```

## 5. Handoff

If the fallback *timing, retries, or conditional order* needs to be documented, keep the model relationships as above and hand off to `create-sequence-view` for the temporal story.
