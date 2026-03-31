No.

`extend frontend -> api 'streams' { ... }` does **not** unambiguously target the async relationship here.

Relationship identity matching is based on **source + target + kind (+ title when needed)**:

- source: `frontend`
- target: `api`
- title: `'streams'`
- kind: differs between the two existing relationships

Given these two existing relationships:

- `frontend -[async]-> api 'streams'`
- `frontend -> api 'streams'`

source, target, and title are the same for both. The **kind** is what distinguishes them. So omitting the kind is **wrong here, not merely ambiguous**, because it can match the unkinded relationship instead of the async one.

The exact extension snippet that unambiguously targets the async relationship is:

```likec4
extend frontend -[async]-> api 'streams' {
  metadata { qos 'high' }
}
```