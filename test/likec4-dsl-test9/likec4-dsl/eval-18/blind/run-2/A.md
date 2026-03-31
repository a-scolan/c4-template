You should **not** use:

`extend frontend -> api 'streams' { metadata { qos 'high' } }`

for the async relationship in this case.

Why: relationship identity matching is based on the combination of:

- **source**
- **target**
- **title**
- **kind**

Here, you already have two distinct relationships with the same:

- source: `frontend`
- target: `api`
- title: `'streams'`

but with different **kinds**:

- `-[async]->`
- `->`

So if you omit the kind in the `extend` statement, you are **not uniquely identifying** the async relationship. In this situation, omitting the kind is **ambiguous, and therefore wrong for targeting the async relationship specifically**.

To unambiguously extend the async relationship, include the same kind in the extension:

`extend frontend -[async]-> api 'streams' {
  metadata {
    qos 'high'
  }
}`
