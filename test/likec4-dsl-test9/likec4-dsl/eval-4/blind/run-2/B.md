1. This styling belongs in that specific view as view-level `style` rules, not in the model or the specification.

2.

```likec4
views {
	view backend-focus {
		include *
		style * { color muted }
		style cloud.backend.* { color primary }
	}
}
```