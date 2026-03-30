`payment.api` → **Invalid** as a single identifier token, because `.` is used to separate FQN path segments (e.g., `cloud.backend`), not inside one identifier.

`1backend` → **Invalid** because identifiers cannot start with a digit.

`payment_api` → **Valid** (`_` is allowed).

`payment-api` → **Invalid** because `-` is not allowed in identifiers.

Rewrites of invalid ones (preserving meaning):
- `payment.api` → `payment_api`
- `1backend` → `backend1`
- `payment-api` → `payment_api`# LikeC4 Identifier Validity

## Rules for LikeC4 Identifiers

LikeC4 identifiers follow these rules:
- Must begin with a letter (`a–z`, `A–Z`) or underscore (`_`)
- Can contain letters, digits (`0–9`), underscores (`_`), and dots (`.`) for qualified/nested names
- **Cannot** start with a digit
- **Cannot** contain hyphens (`-`), which are reserved as an operator

---

## Analysis of Each Identifier

| Identifier    | Valid? | Reason |
|---------------|--------|--------|
| `payment.api` | ✅ Valid | Dot-notation is the standard way to express a nested element (FQN): `api` inside `payment`. |
| `1backend`    | ❌ Invalid | Starts with a digit; identifiers must begin with a letter or underscore. |
| `payment_api` | ✅ Valid | Underscores are allowed and this is a common naming style. |
| `payment-api` | ❌ Invalid | Hyphens are not valid in identifiers; `-` is interpreted as a subtraction/operator character. |

---

## Rewriting Invalid Identifiers

### `1backend` → `backend` or `backend1`

The digit prefix carries no semantic value in most contexts. Move it to the end or drop it:

```
// preferred – drop leading digit
backend

// alternative – move digit to suffix
backend1
```

### `payment-api` → `payment_api`

Replace the hyphen with an underscore to preserve the full meaning:

```
payment_api
```

If the intent was to nest it under a `payment` element, use dot-notation instead:

```
payment.api
```
