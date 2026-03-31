# Identifier validity in LikeC4

LikeC4 identifiers follow this rule:

`^[a-zA-Z_][a-zA-Z0-9_-]*$`

That means an identifier must start with a letter or underscore, may contain letters, digits, underscores, and hyphens, and must not contain dots.

| Identifier | Valid? | Why |
| --- | --- | --- |
| `payment.api` | No | `.` is reserved for FQNs (hierarchy separators), so it is not allowed inside a single identifier. |
| `1backend` | No | Identifiers cannot start with a digit. |
| `payment_api` | Yes | It starts with a letter and uses only allowed characters. |
| `payment-api` | Yes | Hyphens are allowed in identifiers, and it starts with a letter. |

## Rewritten invalid identifiers

- `payment.api` → `payment-api`
- `1backend` → `backend1`
