- `payment.api`: **invalid** — identifiers cannot contain dots (`.`); dots are FQN separators.
- `1backend`: **invalid** — identifiers cannot start with a digit.
- `payment_api`: **valid** — underscores are allowed.
- `payment-api`: **valid** — hyphens are allowed.

Rewrites of invalid identifiers (preserving meaning):
- `payment.api` → `payment_api` (or `payment-api`)
- `1backend` → `backend1`