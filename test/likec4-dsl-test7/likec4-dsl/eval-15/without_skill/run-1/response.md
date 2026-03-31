In LikeC4, a single identifier should use letters/digits/underscore, and must not start with a digit. Dots are used to navigate paths (qualified references), not as part of one identifier token.

- `payment.api` → **Invalid as a single identifier** (contains `.` path separator)
- `1backend` → **Invalid** (starts with a digit)
- `payment_api` → **Valid**
- `payment-api` → **Invalid** (contains `-`)

Rewritten invalid identifiers (preserving meaning):

- `payment.api` → `payment_api`
- `1backend` → `backend1`
- `payment-api` → `payment_api`
