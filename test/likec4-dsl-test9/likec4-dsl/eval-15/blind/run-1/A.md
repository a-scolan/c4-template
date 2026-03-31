# Identifier validity in LikeC4

LikeC4 simple identifiers must start with a letter or `_`, and then may contain letters, digits, and underscores. Dots are used to separate qualified names, and hyphens are not allowed inside a single identifier.

| Candidate | Valid? | Why |
| --- | --- | --- |
| `payment.api` | Invalid as a single identifier | `.` separates a qualified path (`payment` -> `api`) rather than forming one identifier token. |
| `1backend` | Invalid | Identifiers cannot start with a digit. |
| `payment_api` | Valid | It starts with a letter and uses only allowed characters. |
| `payment-api` | Invalid | `-` is not allowed in LikeC4 identifiers. |

## Rewritten invalid identifiers

- `payment.api` -> `payment_api`
- `1backend` -> `backend1`
- `payment-api` -> `payment_api`

If you want to preserve the hierarchical meaning of `payment.api`, model it as two identifiers instead: parent `payment`, child `api`.
