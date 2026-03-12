In `projects/template/system-model.c4`, use a typed arrow and keep the label inline:

```likec4
mySystem.webapp -[calls]-> mySystem.api 'Makes API requests' {
  technology 'HTTPS'
}
```

The relationship type belongs in the arrow (`-[calls]->`), not in the properties block. Keep the action label inline, and keep `technology 'HTTPS'` inside the block. Avoid invalid syntax such as `-> { calls ... }`.
