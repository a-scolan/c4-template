No. Relationship extension matches identity by **source + target + title + kind**. Here you have two relationships with the same source/target/title but different kind (`async` vs default), so omitting kind is **ambiguous and therefore wrong** for targeting the async one.

Use this exact unambiguous extension:

```likec4
extend frontend -[async]-> api 'streams' {
  metadata {
    qos 'high'
  }
}
```# Relationship Identity Matching in LikeC4 `extend`

## The Two Existing Relationships

```likec4
frontend -[async]-> api 'streams'   // kind=async, title=streams
frontend -> api 'streams'           // kind=none (default), title=streams
```

These are **two distinct relationships**. In LikeC4, a relationship's identity is the combination of:

| Field  | Relationship 1     | Relationship 2  |
|--------|--------------------|-----------------|
| source | `frontend`         | `frontend`      |
| target | `api`              | `api`           |
| title  | `'streams'`        | `'streams'`     |
| kind   | `async`            | *(none)*        |

## Can You Use `extend frontend -> api 'streams' { ... }`?

**No.** This snippet targets the **wrong** relationship.

In LikeC4, the arrow syntax is part of the identity:

- `->` means kind = *none* (the default, no explicit kind)
- `-[async]->` means kind = `async`

So `extend frontend -> api 'streams'` matches:

- source = `frontend` ✓
- target = `api` ✓
- title = `'streams'` ✓
- kind = *none* ✓ → matches **Relationship 2**, not Relationship 1

## Is Omitting the Kind Ambiguous or Wrong?

**Wrong**, not merely ambiguous.

Omitting the kind is not a "could match either" situation. The `->` arrow explicitly encodes kind=none, which resolves unambiguously to the no-kind relationship. The async relationship is simply not matched — it is silently skipped. The extension would apply metadata to the wrong relationship without any error or warning.

## Exact Snippet to Target the Async Relationship

```likec4
extend frontend -[async]-> api 'streams' {
  metadata {
    qos 'high'
  }
}
```

The `-[async]->` arrow sets kind=`async`, making all four identity fields match Relationship 1 unambiguously.
