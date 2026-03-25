```likec4
views {
  dynamic order_flow {
    title 'Client → Gateway → Orders → DB'

    client -> gateway 'request'
    gateway -> orders 'forward order request'
    orders -> db 'read/write order'

    db --> orders 'result'
    orders --> gateway 'service response'
    gateway --> client 'HTTP response'
  }
}
```

This is the minimal pattern: use `->` for the request path and `-->` for the return/response arrows so the dynamic view renders like a UML-style sequence.
