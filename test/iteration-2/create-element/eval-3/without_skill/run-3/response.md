Do **not** create two new kinds for this.

Model two **elements** with the same appropriate base kind (usually `externalSystem` for the real third-party payment API and either `externalSystem` or `container` for your internal mock, depending on placement). Then distinguish them with clear names and tags/metadata (for example `env=prod` vs `env=test`, `mock=true`).

So: same kind family, different elements, differentiated by intent via tags/metadata.

For handling the mock-vs-prod modeling pattern, use **implement-pattern**.