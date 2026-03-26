Diagnose this as potentially two independent errors, in order:

1) `Unknown relationship type: sends`
- Relationship kinds are validated against the project specification.
- Check allowed relationship kinds and confirm whether `sends` exists.
- If not declared, replace with a valid kind or declare `sends` in the spec.

2) `Element not found: dataLayer.cache`
- This is id/FQN resolution.
- Verify that `dataLayer.cache` is the exact declared FQN (case-sensitive, correct nesting, correct includes).
- If `cache` is nested elsewhere, use its real full id.

Proper diagnosis flow:
- Fix unknown relationship kind first (parser/model validity).
- Then fix unresolved element FQN with exact declaration lookup.

So yes: it can be both wrong relationship name and broken FQN at the same time.