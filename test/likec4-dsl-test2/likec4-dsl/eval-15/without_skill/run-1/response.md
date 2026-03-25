Valid LikeC4 identifiers here: `payment_api`.

Invalid identifiers:
- `payment.api` — invalid as a single identifier because `.` is used to separate nested element paths / qualified names, not as part of one identifier token.
- `1backend` — invalid because an identifier cannot start with a digit.
- `payment-api` — invalid because `-` is not part of a plain identifier; it is not accepted as an identifier character.

Valid rewrite suggestions that preserve meaning:
- `payment.api` -> `payment_api` (or split it into nested identifiers such as parent `payment` with child `api` if that hierarchy is what you mean)
- `1backend` -> `backend1`
- `payment-api` -> `payment_api`

So, among the four examples, only `payment_api` is already valid.
