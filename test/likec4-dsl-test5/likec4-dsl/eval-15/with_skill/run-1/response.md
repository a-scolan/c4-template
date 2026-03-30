Valid identifiers in LikeC4:
- `payment_api` (valid)
- `payment-api` (valid)

Invalid identifiers:
- `payment.api` (invalid: `.` is reserved as FQN separator, not allowed inside a single identifier)
- `1backend` (invalid: identifiers cannot start with a digit)

Rewrites preserving meaning:
- `payment.api` → `payment_api`
- `1backend` → `backend1`
