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

In the merged model, `port` is **an array with both values**: `['8080', '9090']`.

Why: `extend` merges metadata with the existing element, and when the same metadata key appears multiple times across files, LikeC4 keeps both values by converting that key to an array rather than overwriting the original value.