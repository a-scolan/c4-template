`payment.api` — **invalid**: dots are reserved for FQNs (hierarchy separators), not single identifiers. Rewrite: `payment-api`

`1backend` — **invalid**: identifiers cannot start with a digit. Rewrite: `backend1`

`payment_api` — **valid**: underscores are allowed, and it starts with a letter.

`payment-api` — **valid**: hyphens are allowed, and it starts with a letter.

Rule: LikeC4 identifiers must match `[a-zA-Z_][a-zA-Z0-9_-]*` — start with a letter or underscore, then use only letters, digits, underscores, or hyphens. Dots are only for FQNs.