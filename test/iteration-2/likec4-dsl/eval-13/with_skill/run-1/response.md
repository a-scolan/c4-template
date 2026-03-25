The snippet is invalid because **tags must appear before any properties** inside an element body. The rule states: *TAGS — optional, but must come first if present, before any properties*. Here, `technology 'Node.js'` (a property) appears before `#critical` (a tag), which violates that ordering constraint.

Corrected snippet:
```likec4
model {
  api = service 'API' {
    #critical
    technology 'Node.js'
  }
}
```
Moving `#critical` before `technology` makes the snippet valid.
