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

## Notes

- `customer -> frontend -> api { ... }` is a single chained step expression; the body block applies to the last hop (`frontend -> api`).
- `technology 'HTTPS'` and `navigateTo payment-detail` are declared inside that body.
- `par { ... }` groups the three outgoing steps from `api` as simultaneous (parallel) steps.
