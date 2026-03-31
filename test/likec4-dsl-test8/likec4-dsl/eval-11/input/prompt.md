My `base.c4` defines:
```likec4
model {
  cloud = system 'Cloud' {
    api = service 'API' {
      metadata { port '8080' }
    }
  }
}
```
In `ops.c4` I use `extend cloud.api` to add `metadata { port '9090'; region 'us-east-1' }` and a nested `health = component 'Health Check'`. Show the correct `ops.c4` snippet and state exactly what value `port` holds in the merged model, and why. Be explicit about whether the original `port '8080'` is overwritten or merged.
