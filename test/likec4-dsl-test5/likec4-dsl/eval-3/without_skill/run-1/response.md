```c4
dynamic client_to_db_sequence {
  title "Client order flow"

  client -> gateway "Request"
  gateway -> orders "Forward request"
  orders -> db "Write/read"

  db --> orders "Result"
  orders --> gateway "Response"
  gateway --> client "Final response"
}
```# Minimal LikeC4 Dynamic View – Sequence Diagram

```likec4
dynamic view PlaceOrderSequence {
  title "Place Order – sequence"

  #sequence

  client -> gateway "send request"
  gateway -> orders  "route to orders service"
  orders  -> db      "persist order"
  db      -> orders  "ack"
  orders  -> gateway "order result"
  gateway -> client  "send response"
}
```

## Key points

- `#sequence` tag makes LikeC4 render the dynamic view as a **UML-style sequence diagram** instead of the default flow/C4 style.
- Steps are listed in execution order; arrows declared in **reverse** (`db -> orders -> gateway -> client`) produce the response lane.
- All four elements (`client`, `gateway`, `orders`, `db`) must already be declared somewhere in the model; the dynamic view only references them.
- Optional step labels (the strings after the element pair) appear as message labels on the sequence arrows.
