```likec4
dynamic view orderSequence {
  title 'Order Processing Sequence'

  client -> gateway  'Send request'
  gateway -> orders  'Route to orders service'
  orders -> db       'Persist order'
  db -> orders       'Ack write'
  orders -> gateway  'Return order result'
  gateway -> client  'Return response'

  autoLayout TopBottom
}
```

Notes:
- `dynamic view` is the LikeC4 construct for step-by-step flow / sequence diagrams.
- Steps are numbered implicitly in declaration order.
- Response arrows (db→orders, orders→gateway, gateway→client) are modelled as explicit return steps in reverse direction.
- `autoLayout TopBottom` produces a vertical sequence-like layout. For a strict left-to-right swim-lane appearance use `autoLayout LeftRight`.
