```likec4
dynamic view checkout-flow {
  customer -> frontend -> api {
    technology 'HTTPS'
    navigateTo payment-detail
  }

  api -> {
    payments
    inventory
    notifications
  }
}
```
# Dynamic View: `checkout-flow`

```likec4
dynamic view checkout-flow {
  customer -> frontend -> api {
    technology 'HTTPS'
    navigateTo payment-detail
  }

  par {
    api -> payments
    api -> inventory
    api -> notifications
  }
}
```

**Notes:**
- `customer -> frontend -> api { ... }` is a single chained expression; the body block applies to the final step (`frontend -> api`).
- `technology 'HTTPS'` and `navigateTo payment-detail` are declared inside that body block.
- `par { ... }` groups the three outgoing `api` steps as simultaneous (parallel) fan-out.
