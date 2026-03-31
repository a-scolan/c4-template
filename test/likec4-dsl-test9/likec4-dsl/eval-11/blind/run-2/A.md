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

`port` holds **both values**, so in the merged model it is effectively:

- `port: ['8080', '9090']`

The original `port '8080'` is **not overwritten**. It is **merged** with the new `port '9090'` because duplicate `metadata` keys in LikeC4 merge into an array rather than replacing the earlier value. `region` is added as a new metadata key with value `'us-east-1'`.