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

Splitting this into separate standalone steps would violate the requirement that `customer -> frontend -> api` be expressed as one chained expression with the body attached only to the `frontend -> api` hop.# Dynamic View: checkout-flow

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

Rewriting the chain as separate standalone steps (`customer -> frontend` and `frontend -> api { ... }`) would satisfy neither the single-expression requirement nor keep the body scoped exclusively to the `frontend -> api` hop within a unified chain — the two steps would be independent, losing the structural intent that the chain expresses a single composite flow from customer through frontend to api.
