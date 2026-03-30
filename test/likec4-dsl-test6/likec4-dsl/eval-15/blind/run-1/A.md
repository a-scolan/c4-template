Valid vs invalid identifiers:

- `payment.api` → **Invalid** as a single identifier (`.` is used as a path/FQN separator, not inside one identifier token).
- `1backend` → **Invalid** (identifiers cannot start with a digit).
- `payment_api` → **Valid** (starts with a letter; uses letters/underscore).
- `payment-api` → **Invalid** (hyphen is not allowed in an identifier token).

Rewrites preserving meaning:

- `payment.api` → `payment_api`
- `1backend` → `backend1`
- `payment-api` → `payment_api`
