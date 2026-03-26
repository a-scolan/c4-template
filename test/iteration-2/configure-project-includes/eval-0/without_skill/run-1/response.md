Keep the baseline structure and only make additive changes.

Keep:
- `name`
- `title`
- `extends`
- `include.paths`
- `exclude` (if present)
- `styles` / `relationships` / other existing project-level defaults
- `imageAliases` (existing keys)

Safe include rule:
- Keep shared sources in deterministic order.
- Put the most foundational shared source first (`../shared`), then additional layers.

Suggested pattern:
- `include.paths: ["../shared", "../platform-shared"]`

Image/import safety rules:
- Do not remove or rename existing alias keys used by current diagrams.
- Add new aliases with a namespace prefix (for example `platform_*`) to avoid collisions.
- If two sources define the same alias name, keep current behavior by preserving the existing alias in `imageAliases` and mapping the new source to a new key.

Practical checklist:
1. Add the new path (append, do not reorder existing entries unless required).
2. Keep legacy alias keys unchanged.
3. Introduce new non-conflicting alias keys for new images.
4. Validate by rendering a couple of diagrams that use both old and new aliases.For `projects/payments/likec4.config.json`, keep the baseline fields that control project identity and import resolution:

- `name` (stable project id)
- `title` (optional, human-readable)
- `include.paths` (shared source lookup order)
- `imageAliases` (explicit icon/image alias mapping)
- Any already-used baseline keys like `exclude`, `styles`, `manualLayouts` (keep unchanged unless you need new behavior)

Safe include/image rules:

1. Keep existing `include.paths` entries and order unless you intentionally change precedence.
2. Add new shared sources by appending, not replacing.
3. Keep existing aliases stable (do not repoint existing alias names).
4. Add new aliases with a namespace/prefix (for example `platform.*`) to avoid collisions.
5. Prefer explicit aliases over implicit path-dependent resolution.

Minimal baseline pattern:

- `include.paths`: keep `../shared` and append additional shared folders after it.
- `imageAliases`: preserve current shared aliases, then add new platform aliases under new names.

This prevents broken imports and keeps old diagrams rendering exactly as before.