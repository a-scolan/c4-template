```c4
model {
  client = actor "Client"
  gateway = system "Gateway"
  orders = container "Orders Service"
  db = component "Orders DB"
}

views {
  dynamic order_sequence {
    title "Client order flow"

    client -> gateway "POST /orders"
    gateway -> orders "createOrder()"
    orders -> db "insert order"

    db -> orders "ok"
    orders -> gateway "201 Created"
    gateway -> client "HTTP 201"
  }
}
```

This is the minimal dynamic view flow for `client -> gateway -> orders -> db` plus response arrows back to `client`.