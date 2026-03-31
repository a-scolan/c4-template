Write a dynamic view `checkout-flow` that satisfies all of the following:
- The chain `customer -> frontend -> api` is written using LikeC4's chained step syntax (a single compound expression, not three separate lines).
- The `frontend -> api` step has a body block with `technology 'HTTPS'` and `navigateTo payment-detail`.
- After the chain, `api` fans out simultaneously to `payments`, `inventory`, and `notifications` using the parallel blocks syntax.
Keep the snippet minimal and immediately usable.
