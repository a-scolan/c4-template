Model this with **two explicit read relationships**, not one “smart” relationship.

```likec4
api -[reads]-> redis 'Checks cache' {
  technology 'Redis'
}

api -[reads]-> postgres 'Loads fallback data' {
  technology 'PostgreSQL'
}
```

Guideline:
- Do **not** invent a composite kind like `reads_with_fallback`
- Keep the relationship kind simple and semantic: `reads`
- If you want to hint at fallback behavior, use clear action labels such as `'Checks cache'` and `'Loads fallback data'`

The fallback logic itself is behavioral detail, so it should stay **outside the relationship type**. If you want to show cache miss timing or branching more explicitly, that belongs in a sequence-style interaction view rather than in a custom relationship kind.