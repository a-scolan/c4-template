Wrong: extend frontend -> api 'streams'

That matcher is wrong here because relationship identity includes kind as well as source/target/title, and with both a typed async relationship and an untyped one present, omitting kind can match the untyped relationship instead of the intended async one.

```likec4
extend frontend -[async]-> api 'streams' { metadata { qos 'high' } }
```