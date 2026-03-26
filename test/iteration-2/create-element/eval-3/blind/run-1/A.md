Do not create two kinds.

Model **two elements** (prod + mock) with the same existing kind, then distinguish them with names/tags/metadata.

Example direction:
- `paymentApi` (real provider)
- `paymentApiMock` (test double)

For kind choice and declarations, use **create-element**. For modeling mock-vs-prod as a reusable convention, use **implement-pattern** (tags/metadata pattern).