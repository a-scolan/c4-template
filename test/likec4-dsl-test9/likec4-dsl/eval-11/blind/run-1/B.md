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

`port` holds **both values**, as an array: **`['8080', '9090']`**.

The original `port '8080'` is **not overwritten**. It is **merged** with the new `port '9090'`, because when an element is extended in LikeC4, metadata is merged and **duplicate metadata keys become arrays** rather than using last-write-wins replacement.