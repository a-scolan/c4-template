## Identifier validity analysis

From the skill (Rule 7): *Identifiers allow letters, digits, hyphens, and underscores only. No dots (dots are FQN separators). Cannot start with a digit.*

| Identifier | Valid? | Reason |
|---|---|---|
| `payment.api` | **Invalid** | The dot (`.`) is the FQN separator, not allowed inside a single identifier. |
| `1backend` | **Invalid** | Starts with a digit, which is forbidden. |
| `payment_api` | **Valid** | Letters and underscores only, starts with a letter. |
| `payment-api` | **Valid** | Letters and hyphens only, starts with a letter. |

## Rewrites for invalid identifiers

- `payment.api` → `payment-api` *(hyphen replaces dot; meaning preserved)*
- `1backend` → `backend1` or `backend-1` *(digit moved to the end; meaning preserved)*
