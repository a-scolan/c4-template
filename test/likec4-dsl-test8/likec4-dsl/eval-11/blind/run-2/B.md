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

`port` in the merged model is `['8080', '9090']`.

The original `port '8080'` is **not overwritten**. It is **merged** with `port '9090'`, because `extend cloud.api` merges metadata into the existing element and duplicate metadata keys become arrays. The new `region 'us-east-1'` key is added alongside them.
