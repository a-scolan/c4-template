Valid vs invalid in LikeC4:

- `payment.api` ❌ invalid — dots are reserved as FQN separators, not allowed inside a single identifier.
- `1backend` ❌ invalid — identifiers cannot start with a digit.
- `payment_api` ✅ valid — letters/digits/underscore are allowed.
- `payment-api` ✅ valid — letters/digits/hyphen are allowed.

Rewrites of invalid identifiers (preserving meaning):

- `payment.api` → `payment_api` (or `payment-api`)
- `1backend` → `backend1` (or `backend`)
