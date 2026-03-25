No. The proposed snippet `extend frontend -> api 'streams' { ... }` is invalid. The `extend` syntax for relationships is:

```
extend SOURCE -> TARGET {
  TAGS
  PROPERTIES  // only `metadata` and `link` allowed
}
```

**Matching rules for `extend` on relationships:**
- Matching is done **by SOURCE and TARGET only**.
- The relationship kind (`[async]`) and the title (`'streams'`) are **not part of the extend header** and must not appear there.
- All relationships between the same SOURCE and TARGET pair are extended together; you cannot selectively target one specific kind or title.

**Correct extension snippet:**

```likec4
extend frontend -> api {
  metadata { qos 'high' }
}
```

This will merge `qos 'high'` into the metadata of the existing `frontend -[async]-> api 'streams'` relationship. If there are multiple relationships between `frontend` and `api`, the metadata is merged into all of them.
