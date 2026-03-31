The correct `ops.c4` snippet is:

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

In the merged model, `port` holds exactly `'9090'`.

Why:

- `extend cloud.api` adds to the existing `cloud.api` element.
- The metadata is merged by key.
- `region 'us-east-1'` is added because `region` did not exist before.
- For the duplicate key `port`, the later value from the extension wins.

So the original `port '8080'` is **overwritten/replaced** by `port '9090'`; it is **not** kept as both values and it is **not** merged into a multi-value field.