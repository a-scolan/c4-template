`payment.api` — **valid**. Dots are allowed to qualify/nest identifiers, and both `payment` and `api` are valid identifier parts.

`1backend` — **invalid**. LikeC4 identifiers cannot start with a digit.

`payment_api` — **valid**. Underscores are allowed in identifiers.

`payment-api` — **invalid**. Hyphens are not allowed inside identifiers.

Valid rewrites for the invalid identifiers:

- `1backend` → `_1backend` (or `backend_1`)
- `payment-api` → `payment_api`
