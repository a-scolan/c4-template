# Minimal LikeC4 Dynamic View — UML Sequence

Use `dynamic view` with `variant sequence` to render as a UML-style sequence diagram. Forward steps use `->` ; response arrows use `<-` (syntactic reversal: `A <- B` means B sends a message to A).

```likec4
dynamic view order-flow {
  variant sequence

  client -> gateway "request"
  gateway -> orders "forward"
  orders -> db "query"
  orders <- db "result"
  gateway <- orders "response"
  client <- gateway "reply"
}
```

## Key points

| Element | Explanation |
|---|---|
| `dynamic view` | Required wrapper for interaction/flow diagrams |
| `variant sequence` | Switches rendering to UML sequence diagram (lifelines + arrows) |
| `A -> B "label"` | Forward step from A to B |
| `A <- B "label"` | Response step: B sends back to A (arrow drawn from B's lifeline to A's) |

The `variant sequence` property is what distinguishes this from an animated flow diagram — without it, LikeC4 renders the same steps as a box-and-arrow flow, not a UML sequence.
