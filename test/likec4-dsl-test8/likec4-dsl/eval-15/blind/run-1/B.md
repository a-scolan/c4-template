- `payment.api` — **invalid**: dots are reserved for FQN hierarchy separators, not allowed inside a single identifier.
- `1backend` — **invalid**: identifiers cannot start with a digit.
- `payment_api` — **valid**: underscores are allowed, and it starts with a letter.
- `payment-api` — **valid**: hyphens are allowed, and it starts with a letter.

Rewrites of the invalid ones while preserving meaning:
- `payment.api` → `payment-api`
- `1backend` → `backend1`