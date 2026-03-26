`ops.c4`:

```likec4
model {
  extend cloud.api {
    metadata {
      port "9090"
      region "us-east-1"
    }
    health = component "Health Check"
  }
}
```

Merged `port` becomes an array: `['8080', '9090']`, because duplicate metadata keys merge into arrays.