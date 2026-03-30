- `payment.api` — invalid. Dots are not allowed in identifiers; dots are reserved for FQNs.
- `1backend` — invalid. An identifier cannot start with a digit.
- `payment_api` — valid. Underscores are allowed.
- `payment-api` — valid. Hyphens are allowed.

Rewritten invalid identifiers:
- `payment.api` → `payment_api`
- `1backend` → `backend1`