In LikeC4, identifiers should start with a letter or underscore, then use letters, digits, or underscores. Dots are used for qualified paths (e.g., nested element references), not hyphens.

- `payment.api` ✅ valid as a qualified identifier/path (segment identifiers are valid).
- `1backend` ❌ invalid: starts with a digit.
- `payment_api` ✅ valid: uses letters + underscore.
- `payment-api` ❌ invalid: hyphen (`-`) is not allowed in identifiers.

Rewritten invalid identifiers (same meaning):

- `1backend` → `backend1`
- `payment-api` → `payment_api`
