`payment.api` → **Invalid** (dots are reserved as FQN separators, not allowed inside a single identifier)

`1backend` → **Invalid** (identifiers cannot start with a digit)

`payment_api` → **Valid** (letters/digits/underscore are allowed)

`payment-api` → **Valid** (letters/digits/hyphen are allowed)

### Rewrites for invalid identifiers (same meaning)

- `payment.api` → `payment_api` (or `payment-api`)
- `1backend` → `backend1` (or `backend`)
