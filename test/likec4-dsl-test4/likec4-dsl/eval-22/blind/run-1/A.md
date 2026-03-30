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

Rewriting the chain as separate standalone steps (`customer -> frontend` and `frontend -> api { ... }`) would not satisfy the request because a chained expression (`customer -> frontend -> api`) defines a single sequential flow where the body applies to the last hop of the chain, whereas two separate steps are treated as independent, unrelated transitions with no implied sequencing between them.
