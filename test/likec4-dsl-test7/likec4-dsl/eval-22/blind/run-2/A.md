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

Rewriting the chain as separate standalone steps would violate the requirement to keep `customer -> frontend -> api` as one single chained expression and would no longer test hop-scoped body attachment on only `frontend -> api` in that exact chain form.
