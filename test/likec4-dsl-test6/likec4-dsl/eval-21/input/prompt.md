Given this base view:
```likec4
view backend-overview of cloud.backend {
  include *
}
```
Is the following child view valid as written, or does it need `of cloud.backend` again?
```likec4
view backend-detail extends backend-overview {
  include api
}
```
Answer first with `Valid as written.` or `Needs scope redeclared.` Then explain why in one short paragraph and show the smallest final snippet that also adds incoming relationships to `cloud.backend`.
