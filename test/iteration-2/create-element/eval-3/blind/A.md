Do not create two kinds for this.

Reuse one existing workspace kind for both elements:

- use `System_External` if both represent external payment APIs, or
- use `Container_Api` if both are internal APIs inside your system.

If the real payment API and the mock variant have different responsibilities or are modeled as separate integrations, create two elements—not two kinds. For example, avoid inventing a `Container_MockApi` kind.

To distinguish mock vs prod, use view context or an approved tag where needed, rather than a dedicated kind.

Use `create-element` for the element declarations themselves. If the difference is about environment or runtime placement, handle that with `model-deployment-infrastructure`; if it is mainly about what to show to readers, separate it in the relevant view design.