ops.c4

model {
  extend cloud.api {
    metadata {
      port '9090'
      region 'us-east-1'
    }

    health = component 'Health Check'
  }
}

`port` holds `['8080', '9090']` in the merged model. The original `port '8080'` is not overwritten. LikeC4 merges duplicate metadata keys into arrays when you `extend` an element, so both `port` values are preserved.
