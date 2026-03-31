```likec4
views {
  dynamic client_gateway_orders_db {
    title 'Client → Gateway → Orders → DB'

    client -> gateway 'Request'
    gateway -> orders 'Forward request'
    orders -> db 'Query / write'

    db -> orders 'Result'
    orders -> gateway 'Service response'
    gateway -> client 'HTTP response'
  }
}
```