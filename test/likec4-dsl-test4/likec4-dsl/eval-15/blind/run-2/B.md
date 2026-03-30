# LikeC4 Identifier Validity

## Analysis

| Identifier | Valid? | Reason |
|---|---|---|
| `payment.api` | **Valid** | Dot notation is used in LikeC4 to represent hierarchical/nested element paths (e.g., `payment.api` refers to the `api` element nested under `payment`). This is valid and idiomatic in LikeC4. |
| `1backend` | **Invalid** | Identifiers must start with a letter (a–z, A–Z) or underscore `_`. Starting with a digit is not allowed. |
| `payment_api` | **Valid** | Underscores are allowed in identifiers. This is a valid flat identifier. |
| `payment-api` | **Invalid** | Hyphens (`-`) are not valid in LikeC4 identifiers. They are not part of the allowed character set for names. |

## Rewriting Invalid Identifiers

| Original | Valid Rewrite | Notes |
|---|---|---|
| `1backend` | `backend` or `one_backend` | Remove the leading digit, or replace it with a word prefix. `backend` is the simplest meaningful option. |
| `payment-api` | `payment_api` or `paymentApi` | Replace the hyphen with an underscore (snake_case) or use camelCase. Both are valid. |

## Summary

Valid LikeC4 identifiers follow these rules:
- Must **start** with a letter (`a–z`, `A–Z`) or underscore `_`
- Can contain letters, digits, and underscores after the first character
- **Dot** (`.`) is not an identifier character per se but is used as a **path separator** to reference nested elements
- **Hyphens** (`-`) and **leading digits** are not allowed
