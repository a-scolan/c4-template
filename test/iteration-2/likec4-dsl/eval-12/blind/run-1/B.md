Not the same way as element views.

Use direct deployment-view rules instead:

```likec4
deployment view prod-deploy {
  include prod.**
  style prod.** { color red }
}
```

Not supported in deployment views (for this case):
- `include ... with { ... }` customization form.
- `global style myTheme` application pattern used for element-view style groups.