No.

`extend` matches an existing relationship by its full identity: source, target, title, and kind. Here you already have two relationships with the same source (`frontend`), target (`api`), and title (`'streams'`), but with different kinds (`async` and the default kind), so omitting the kind does not uniquely identify the async relationship. In this situation, omitting the kind is ambiguous and therefore wrong.

Use this exact extension snippet:

```likec4
extend frontend -[async]-> api 'streams' {
  metadata {
    qos 'high'
  }
}
```