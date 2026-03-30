## Minimal LikeC4 Dynamic View — UML Sequence

```likec4
views {
  dynamic view order-flow {
    variant sequence

    client -> gateway "send request"
    gateway -> orders "route"
    orders -> db "query"
    orders <- db "rows"
    gateway <- orders "data"
    client <- gateway "response"
  }
}
```

### Key points

| Construct | Purpose |
|---|---|
| `dynamic view` | Declares an interaction/flow view |
| `variant sequence` | Switches rendering to UML-style sequence diagram (lifelines + arrows) |
| `A -> B "label"` | Forward step (request direction) |
| `A <- B "label"` | Backward/response arrow (B returns to A) |

The four forward steps establish the call chain `client → gateway → orders → db`.  
The three backward steps (`orders <- db`, `gateway <- orders`, `client <- gateway`) carry the response back up the chain to the original caller.
