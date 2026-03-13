1. probable error category: relationship taxonomy error plus possible FQN error.
2. root cause: `sends` is not one of the shared model relationship types in this workspace. The declared logical relationships are `uses`, `calls`, `async`, `reads`, and `writes`, so `sends` must be mapped to the real intent instead of accepted as-is. Separately, `dataLayer.cache` may be a broken FQN: either `dataLayer` is not the real parent, or `cache` is named differently / lives elsewhere.
3. verification step: first check the relationship taxonomy in `projects/shared/spec-global.c4` or `projects/shared/SPEC_CHEATSHEET.md`. Then inspect the model hierarchy and verify whether a real element exists at `dataLayer.cache`; if not, find the actual full name such as `system.cache` or `system.dataLayer.cache`.
4. minimal fix: correct the relationship kind based on semantics, then correct the target to the real FQN. For example, if this is asynchronous messaging:
`producer -[async]-> actualSystem.actualCache 'Publishes invalidation' { technology 'AMQP' }`
If it is cache access rather than messaging, use `-[reads]->` or `-[writes]->` against the real cache element FQN.
