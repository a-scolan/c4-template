# LikeC4 Identifier Validity

## Rules (from the DSL spec)

An identifier must:
- Contain only **letters, digits, hyphens, and underscores**
- **Not start with a digit**
- Contain **no dots** (dots are FQN separators, not part of an identifier)

---

## Analysis

| Identifier    | Valid? | Reason |
|---------------|--------|--------|
| `payment.api` | **Invalid** | Dot is the FQN separator; it cannot appear inside a single identifier |
| `1backend`    | **Invalid** | Identifiers cannot start with a digit |
| `payment_api` | **Valid**   | Underscores are allowed; starts with a letter |
| `payment-api` | **Valid**   | Hyphens are allowed; starts with a letter |

---

## Rewrites of invalid identifiers

- `payment.api` → `payment-api`  
  (replace the dot with a hyphen, which is the idiomatic separator in LikeC4)

- `1backend` → `backend-1`  
  (move the digit to the end and separate with a hyphen to preserve the "backend #1" meaning)
