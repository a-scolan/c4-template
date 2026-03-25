No — not as written.

For relationship `extend`, LikeC4 matches an existing relationship by its **full relationship signature** (source, target, and relationship identity such as kind/label tuple). If multiple relationships could match, extension must be specific enough to resolve to exactly one. If nothing matches exactly, the `extend` fails.

Your existing relationship is:

`frontend -[async]-> api 'streams'`

So the extension should include the same relationship identity:

`extend frontend -[async]-> api 'streams' { metadata { qos 'high' } }`