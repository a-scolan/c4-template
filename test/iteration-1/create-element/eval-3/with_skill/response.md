Use **two elements, not two kinds**.

Reuse the same existing repository kind for both, for example `Container_Api`, and model them as separate elements if they have distinct responsibilities or endpoints:

- `paymentApi` → real payment integration
- `mockPaymentApi` → test/mock variant

Do **not** introduce a special kind such as `Container_MockApi` just to represent the mock.

If you need to distinguish mock vs prod in documentation, use **tags and/or view context**, not a dedicated kind. If the difference is mainly about environment or runtime placement, handle that with **`model-deployment-infrastructure`**. If the difference is mainly about what to show to readers, handle it with **`design-view`**.