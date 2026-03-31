- `payment.api` — **Valid** as a qualified identifier/reference. Each segment (`payment` and `api`) is a valid identifier, and `.` is used to separate nested names.
- `1backend` — **Invalid** because a LikeC4 identifier cannot start with a digit.
- `payment_api` — **Valid** because identifiers may contain letters, digits, and underscores, and this one starts with a letter.
- `payment-api` — **Invalid** because `-` is not allowed in identifiers.

Rewritten invalid identifiers:
- `1backend` → `_1backend`
- `payment-api` → `payment_api`
