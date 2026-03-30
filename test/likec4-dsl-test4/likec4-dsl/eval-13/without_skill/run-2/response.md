## Why it is invalid

In LikeC4 DSL, tags (`#tagname`) are part of the **element header**, not the element body block. Placing `#critical` as a standalone line inside the `{ … }` body is a syntax error.

Tags must be declared **inline, after the element title**, on the same line as the opening brace.

## Corrected snippet

```likec4
model {
  api = service 'API' #critical {
    technology 'Node.js'
  }
}
```

The only change is moving `#critical` from inside the body to after the title `'API'`, where tags are syntactically expected.
