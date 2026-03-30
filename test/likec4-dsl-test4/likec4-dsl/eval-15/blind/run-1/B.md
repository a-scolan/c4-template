# Identifier Validity in LikeC4

LikeC4 identifier rules (from the DSL spec):
- **Allowed characters:** letters, digits, hyphens (`-`), underscores (`_`).
- **Cannot start with a digit.**
- **Dots are forbidden** — dots are FQN (Fully Qualified Name) separators, not part of an identifier.

---

## Analysis

| Identifier    | Valid? | Reason                                                                 |
|---------------|--------|------------------------------------------------------------------------|
| `payment.api` | ❌ Invalid | Contains a dot. Dots are FQN separators, not identifier characters. `payment.api` would be parsed as the child element `api` inside parent `payment`, not as a single identifier. |
| `1backend`    | ❌ Invalid | Starts with a digit. Identifiers cannot begin with a digit.            |
| `payment_api` | ✅ Valid   | Uses only letters and underscores. No digit start, no dot.             |
| `payment-api` | ✅ Valid   | Uses only letters and a hyphen. No digit start, no dot.                |

---

## Rewrites for Invalid Identifiers

- `payment.api` → **`payment-api`** (replace dot with hyphen; preserves both words and their meaning)
- `1backend` → **`backend1`** (move digit to end; preserves the word "backend")
