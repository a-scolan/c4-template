- `payment.api` is **invalid** as an identifier because `.` is used as a path separator in FQNs, not inside a single identifier.
- `1backend` is **invalid** because identifiers cannot start with a digit.
- `payment_api` is **valid**.
- `payment-api` is **invalid** because `-` is not allowed in identifiers.

Valid rewrites (preserving meaning):
- `payment.api` -> `payment_api`
- `1backend` -> `backend1`
- `payment-api` -> `payment_api`
# LikeC4 Identifier Validity

## Rules

LikeC4 identifiers must:
- Start with a letter (`a-z`, `A-Z`) or underscore (`_`)
- Contain only letters, digits (`0-9`), and underscores
- Not use dots (`.`) — dots are the **namespace separator** (FQN path delimiter), not part of a bare identifier
- Not use hyphens (`-`) — hyphens are not valid identifier characters in LikeC4

---

## Analysis

| Identifier    | Valid? | Reason |
|---------------|--------|--------|
| `payment.api` | **No** | Dot is the namespace separator; this is parsed as element `api` nested inside `payment`, not a single flat identifier |
| `1backend`    | **No** | Starts with a digit — identifiers must start with a letter or underscore |
| `payment_api` | **Yes** | Starts with a letter, contains only letters and underscores — fully valid |
| `payment-api` | **No** | Hyphen is not an allowed character in LikeC4 identifiers |

---

## Rewrites

| Original      | Valid Rewrite     | Notes |
|---------------|-------------------|-------|
| `payment.api` | `payment_api`     | Replace dot with underscore to form a single flat identifier |
| `1backend`    | `backend1`        | Move digit to end; or use `one_backend` if the "1" carries semantic meaning |
| `payment-api` | `payment_api`     | Replace hyphen with underscore |

### Example in context

```likec4
model {
  // invalid originals (would cause parse errors as flat ids)
  // payment.api   -- parsed as nested reference, not a declaration
  // 1backend      -- syntax error
  // payment-api   -- syntax error

  // valid rewrites
  payment_api = component "Payment API"
  backend1    = component "1Backend Service"
}
```

> Note: `payment.api` **is** valid as a fully-qualified name (FQN) when *referencing* a nested element (e.g., `payment` contains `api`), but it cannot be used as a standalone identifier in a declaration.
