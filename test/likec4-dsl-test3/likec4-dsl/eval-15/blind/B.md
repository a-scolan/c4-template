- `payment.api` ✅ **Valid** as a qualified identifier (dot-separated path), where each segment (`payment`, `api`) is a valid identifier.
- `1backend` ❌ **Invalid** because identifiers cannot start with a digit.
- `payment_api` ✅ **Valid** because underscores are allowed.
- `payment-api` ❌ **Invalid** because `-` is not allowed in identifiers.

Rewrites of invalid identifiers:
- `1backend` → `backend1`
- `payment-api` → `payment_api`
