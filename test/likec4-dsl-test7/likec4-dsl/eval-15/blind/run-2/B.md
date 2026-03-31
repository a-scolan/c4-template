- `payment.api` — **invalid**: dots are reserved as FQN separators, so a single identifier cannot contain `.`
- `1backend` — **invalid**: an identifier cannot start with a digit
- `payment_api` — **valid**: letters, digits, and underscores are allowed
- `payment-api` — **valid**: letters, digits, and hyphens are allowed

Rewritten invalid identifiers:
- `payment.api` → `payment_api`
- `1backend` → `backend1`
