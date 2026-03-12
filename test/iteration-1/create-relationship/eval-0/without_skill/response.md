Use the typed arrow exactly like this in `projects/template/system-model.c4`:

```likec4
mySystem.webapp -[calls]-> mySystem.api 'Makes API requests' {
  technology 'HTTPS'
}
```

The relationship type belongs in the arrow itself: `-[calls]->`.

Keep the human-readable label inline after the target, and put protocol details such as `technology 'HTTPS'` in the properties block.

Do not use invalid forms such as `-> { calls ... }` or move `calls` into the block.