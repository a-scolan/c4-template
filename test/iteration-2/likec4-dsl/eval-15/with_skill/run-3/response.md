Validity:
- `payment.api` ❌ invalid (`.` is not allowed in identifiers; dot is FQN separator).
- `1backend` ❌ invalid (cannot start with a digit).
- `payment_api` ✅ valid.
- `payment-api` ✅ valid.

Valid rewrites preserving meaning:
- `payment.api` → `payment_api`
- `1backend` → `backend1`