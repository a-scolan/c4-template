`payment.api` → **Invalid**: dot (`.`) is not allowed in a single identifier (it is used as an FQN separator).

`1backend` → **Invalid**: identifiers cannot start with a digit.

`payment_api` → **Valid**: uses allowed characters (letters, digits, underscore), and does not start with a digit.

`payment-api` → **Valid**: uses allowed characters (letters, digits, hyphen), and does not start with a digit.

Rewrites for invalid ones (preserving meaning):
- `payment.api` → `payment_api` (or `payment-api`)
- `1backend` → `backend1`