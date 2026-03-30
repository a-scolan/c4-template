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

Rewriting as separate standalone steps (`customer -> frontend`, then `frontend -> api { ... }`) would break the requirement because a chained expression `A -> B -> C { ... }` attaches the body exclusively to the last hop (`B -> C`), which cannot be expressed with two independent step declarations without losing that semantic attachment.
