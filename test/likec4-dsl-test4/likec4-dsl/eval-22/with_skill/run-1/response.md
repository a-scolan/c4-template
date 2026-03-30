```likec4
dynamic view checkout-flow {
  customer -> frontend "start checkout" -> api "submit order" {
    technology 'HTTPS'
    navigateTo payment-detail
  }

  parallel {
    api -> payments "process payment"
    api -> inventory "reserve items"
    api -> notifications "send confirmation"
  }
}
```

Rewriting the chain as three separate standalone steps would not satisfy the request because requirement (1) explicitly demands a **single chained expression** — a contiguous chain statement where each `->` hop extends the same expression — and splitting it into `customer -> frontend` followed by `frontend -> api` as independent lines violates that structural constraint, even though both renderings produce identical diagrams.
