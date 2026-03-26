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
4. Validate by rendering a couple of diagrams that use both old and new aliases.