```likec4
dynamic view checkout-flow {
  customer -> frontend -> api {
    technology 'HTTPS'
    navigateTo payment-detail
  }

  parallel {
    api -> payments
    api -> inventory
    api -> notifications
  }
}
```

Rewriting the chain into separate standalone steps would break the requirement that `customer -> frontend -> api` is expressed as one single chained statement with metadata attached only to the `frontend -> api` hop.# Dynamic View: checkout-flow

## Snippet

```likec4
dynamic view checkout-flow {

  // (1) single chained expression; (2) body applies only to the frontend -> api hop
  customer -> frontend -> api {
    technology 'HTTPS'
    navigateTo payment-detail
  }

  // (3) api fans out in parallel
  parallel {
    api -> payments
    api -> inventory
    api -> notifications
  }
}
```

## Why separate standalone steps would not satisfy the request

Rewriting `customer -> frontend -> api { ... }` as two standalone steps (`customer -> frontend` and `frontend -> api { ... }`) would satisfy requirements (2) and (3) individually, but would violate requirement (1), which explicitly demands a single chained expression that expresses both hops as one connected traversal rather than two independent declarations.
