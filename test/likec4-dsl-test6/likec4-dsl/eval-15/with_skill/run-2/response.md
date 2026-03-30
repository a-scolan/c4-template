- `payment.api` — **invalid**. `.` is reserved as an FQN separator, so it cannot appear inside a single identifier.
- `1backend` — **invalid**. Identifiers cannot start with a digit.
- `payment_api` — **valid**. Letters, digits, and underscores are allowed.
- `payment-api` — **valid**. Letters, digits, and hyphens are allowed.

Rewritten invalid identifiers:
- `payment.api` → `payment-api`
- `1backend` → `backend-1`
