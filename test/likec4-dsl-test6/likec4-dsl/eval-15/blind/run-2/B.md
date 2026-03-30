As **single LikeC4 identifiers**:

- `payment.api` — **Invalid** as a single identifier. The dot is used to separate qualified names / nested paths, not to form one identifier token.
- `1backend` — **Invalid**. Identifiers cannot start with a digit.
- `payment_api` — **Valid**. Underscores are allowed.
- `payment-api` — **Invalid**. Hyphens are not allowed in identifiers.

Possible valid rewrites that preserve meaning:

- `payment.api` → `payment_api`
- `1backend` → `backend1`
- `payment-api` → `payment_api`
