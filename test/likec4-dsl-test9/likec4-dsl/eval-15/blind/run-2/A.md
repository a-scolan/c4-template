| Identifier | Valid? | Why |
|---|---|---|
| `payment.api` | Invalid | Dots are not allowed inside a single LikeC4 identifier; `.` is reserved as an FQN separator between hierarchy levels. |
| `1backend` | Invalid | A LikeC4 identifier cannot start with a digit. |
| `payment_api` | Valid | Underscores are allowed, and it starts with a valid character. |
| `payment-api` | Valid | Hyphens are allowed, and it starts with a valid character. |

Invalid ones rewritten into valid identifiers while preserving meaning:

- `payment.api` → `payment-api`
- `1backend` → `backend1`
