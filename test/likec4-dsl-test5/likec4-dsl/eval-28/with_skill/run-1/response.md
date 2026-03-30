Wrong: extend frontend -> api 'streams'
When both a typed and an untyped relationship share the same source, target, and title, omitting kind is wrong because relationship identity includes kind, so this matcher can bind to the untyped relation instead of the intended async one.

```likec4
extend frontend -[async]-> api 'streams' { metadata { qos 'high' } }
```