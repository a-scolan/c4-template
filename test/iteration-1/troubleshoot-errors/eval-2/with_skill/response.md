1. Probable error category: both taxonomy and FQN.
2. Root cause: `sends` is not one of the declared model relationship kinds in this workspace. The valid model kinds are `uses`, `calls`, `async`, `reads`, and `writes`. `dataLayer.cache` may also be a broken FQN because `cache` is not actually nested under `dataLayer`, or `dataLayer` itself is not the full path from the model root.
3. Verification step: first check the relationship table in `projects/shared/SPEC_CHEATSHEET.md` to choose the correct interaction kind. Then inspect the cache declaration and copy its full FQN exactly as declared.
4. Minimal fix: replace `sends` with the correct model relationship kind, and replace `dataLayer.cache` with the actual full FQN.
Examples:
- If this is asynchronous messaging: `producer -[async]-> <full.cache.fqn> 'Publishes event'`
- If this is cache access: `api -[reads]-> <full.cache.fqn> 'Reads cached data'`
The clean diagnosis is: do not guess either piece—validate the relationship kind from the shared spec, then validate the element path from the declaration hierarchy.
