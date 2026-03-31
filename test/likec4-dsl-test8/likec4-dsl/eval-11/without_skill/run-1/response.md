`ops.c4`

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

In the merged model, `port` holds exactly **`'9090'`**.

Why:
- the `metadata` blocks are **merged by key**
- `region` is added as a new metadata entry
- `port` uses the **same key** as in `base.c4`, so the later value from `extend cloud.api` **overwrites** the original one

So the original `port '8080'` is **not preserved alongside** `port '9090'`, and it is **not merged into multiple values**. It is simply **overwritten** by `port '9090'`.