**Correct `ops.c4` snippet:**

```likec4
model {
  extend cloud.api {
    metadata {
      port '9090'
      region 'us-east-1'
    }
    health = component 'Health Check'
  }
}
```

**Value of `port` in the merged model:** `['8080', '9090']` — an array containing both values.

**Why:** The SKILL.md decision tree states explicitly: *"Metadata merge → Duplicate keys become arrays"*. `extend` is only allowed to contribute `metadata` and `link` as properties; it cannot override other properties. When `ops.c4` extends `cloud.api` with `metadata { port '9090' }`, LikeC4 does not replace the existing `port '8080'` from `base.c4` — instead, it collects both string values into an array: `['8080', '9090']`. `region` is a new key with no prior value, so it remains the plain string `'us-east-1'`.

**Note on the snippet:** The semicolons used in the prompt (`port '9090'; region 'us-east-1'`) are not valid LikeC4 metadata syntax. Metadata entries are separated by whitespace/newlines, not semicolons. The corrected snippet above uses the proper multi-line form.
