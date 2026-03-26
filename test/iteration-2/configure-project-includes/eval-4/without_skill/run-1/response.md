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
- New source adoption = new alias names, not in-place replacement.If `../platform-shared` redefines aliases from `../shared`, keep current resolution stable by treating this as a non-breaking migration:

1. `include.paths`
- Keep `../shared` first.
- Append `../platform-shared` after it (or keep it after if already present).
- Do not prepend `../platform-shared` unless you intentionally want override behavior.

2. `imageAliases`
- Keep existing alias keys that currently point to `../shared/...` exactly as they are.
- Add new platform-specific aliases under new names (for example `platform.aws.lambda`, `platform.azure.fn`).
- Do not map platform files onto existing shared alias names.

3. Collision handling rule
- Existing alias name = frozen contract.
- New source gets new alias namespace.

This preserves all existing diagrams while still enabling new assets from platform-shared.