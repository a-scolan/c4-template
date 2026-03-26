Identifier rules: start with a letter/underscore, then letters/digits/underscores only.

- `payment.api` ❌ (dot not allowed in identifiers)
- `1backend` ❌ (cannot start with digit)
- `payment_api` ✅
- `payment-api` ❌ (hyphen not allowed)

Valid rewrites:
- `payment.api` → `payment_api`
- `1backend` → `backend1`
- `payment-api` → `payment_api`