ops.c4:

extend cloud.api {
  metadata {
    port '9090'
    region 'us-east-1'
  }

  health = component 'Health Check'
}

In the merged model, `port` holds `9090`.

Why: `extend cloud.api` merges into the existing `cloud.api` element. The new child `health` is added, and metadata entries are merged by key. When the same metadata key appears again (`port`), the value from the extension overrides the earlier one from `base.c4`. The new `region` key is added alongside it.
