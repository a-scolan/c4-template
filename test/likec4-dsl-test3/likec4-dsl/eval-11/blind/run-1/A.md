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

In the merged model, `port` is **both values** (an array): `['8080', '9090']`.

Why: `extend` merges metadata (it does not replace the original metadata object), and when the same metadata key appears multiple times across files, LikeC4 keeps all values by turning that key into an array.