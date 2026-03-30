Correct matcher: extend frontend -[async]-> api 'streams'

`extend frontend -> api 'streams'` is insufficient because source, target, and title are not enough to uniquely identify the intended relationship when multiple relationships exist between the same endpoints with the same title but different kinds. `extend frontend -[sync]-> api 'streams'` targets the wrong relationship because it explicitly matches the `sync` kind, not `async`.

```likec4
extend frontend -[async]-> api 'streams' {
	metadata { qos 'high' }
}
```
Error: Unable to read eval prompt in this benchmark mode due read-scope restrictions (with_skill_targeted), so no prompt-specific answer could be generated.