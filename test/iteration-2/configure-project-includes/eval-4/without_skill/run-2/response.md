Use an additive merge with explicit alias conflict handling.

`include.paths`:
- Keep `../shared` first.
- Append `../platform-shared` after it.
- Do not reorder existing entries unless you want different precedence semantics.

`imageAliases` with collisions:
- Keep all currently used alias keys mapped as-is.
- For aliases redefined by `../platform-shared`, introduce a namespaced key for the platform image (for example `platform_db`, `platform_queue`, etc.).
- Update only new diagrams to use the new namespaced keys; old diagrams keep working unchanged.

Rule of thumb:
- Backward compatibility = existing alias keys stay stable.
- New source adoption = new alias names, not in-place replacement.