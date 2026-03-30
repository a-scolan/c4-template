# LikeC4 Identifier Validity

## Analysis

In LikeC4, identifiers follow standard programming language conventions: they must start with a letter or underscore, and can contain letters, digits, and underscores. Dots (`.`) are used as namespace/hierarchy separators, and hyphens (`-`) are **not** valid in identifiers.

| Identifier | Valid? | Reason |
|---|---|---|
| `payment.api` | ✅ Valid | Dot separates namespace segments; each segment (`payment`, `api`) is a valid identifier |
| `1backend` | ❌ Invalid | Starts with a digit; identifiers must begin with a letter or underscore |
| `payment_api` | ✅ Valid | Underscore is allowed; starts with a letter |
| `payment-api` | ❌ Invalid | Hyphen (`-`) is not a valid character in LikeC4 identifiers |

## Rewrites

- `1backend` → `backend` or `_1backend` or `one_backend` (remove or replace the leading digit)
- `payment-api` → `payment_api` (replace hyphen with underscore)
