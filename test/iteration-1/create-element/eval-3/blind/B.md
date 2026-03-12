Use existing kinds, not new ones.

If the real payment API and the mock variant represent different responsibilities or endpoints, model them as two separate elements, but reuse the same existing kind for both. For example:

- use `Container_Api` for both if they are internal services
- use `System_External` for the real payment API if it is a third-party provider, and `Container_Api` for your internal mock if needed

Do not create a special mock kind such as `Container_MockApi`.

To show mock vs prod, use names, tags, or separate views. Keep element creation focused on the declarations, and handle environment or deployment differences in deployment modeling or dedicated environment views.