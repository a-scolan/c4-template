```likec4
views {
  dynamic order_sequence {
    title 'client -> gateway -> orders -> db'

    client -> gateway 'request'
    gateway -> orders 'forward'
    orders -> db 'query'

    db -> orders 'result'
    orders -> gateway 'response'
    gateway -> client 'response'
  }
}
```