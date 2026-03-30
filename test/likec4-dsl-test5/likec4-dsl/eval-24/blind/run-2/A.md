Correct matcher: extend frontend -[async]-> api 'streams'

`extend frontend -> api 'streams'` is insufficient because relationship identity matching must include kind when multiple same source/target/title relationships exist, and `extend frontend -[sync]-> api 'streams'` targets the different `sync` relationship, not the `async` one.

```likec4
extend frontend -[async]-> api 'streams' {
  metadata { qos 'high' }
}
```