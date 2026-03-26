Follow additive, non-breaking edit rules.

For `include.paths`:
- Keep existing entries untouched and in place.
- Append new shared source after current ones unless you intentionally want precedence changes.
- Use normalized relative paths only.

For icons/images:
- Do not overwrite existing alias keys.
- Add new aliases with a source prefix (`platform_...`) to prevent collisions.
- If both shared sources export similarly named images, explicitly map both with distinct alias keys.

Change strategy:
1. Backup current config.
2. Add one source path.
3. Add only the new alias mappings needed for that source.
4. Validate diagrams referencing legacy aliases (must still resolve).
5. Validate at least one diagram using a new alias.

Avoid:
- Reordering existing include paths accidentally.
- Renaming existing aliases in-place.
- Mixing multiple risky changes in one commit.Given `include.paths: ['../shared', '../platform-shared']`, follow these edit rules to add another shared source safely:

- Preserve existing order and append the new source at the end unless precedence must change.
- Never remove or reorder existing paths during a compatibility edit.
- Keep all existing `imageAliases` mappings untouched.
- Add aliases for the new source with a distinct prefix (for example `newshared.*`).
- Do not reuse existing alias names even if files look equivalent.
- If two sources define similar assets, pin old aliases to old source and introduce new alias names for new source.

Safe pattern:

- Before: `['../shared', '../platform-shared']`
- After: `['../shared', '../platform-shared', '../new-shared']`

And in `imageAliases`:

- keep current entries unchanged
- add only new prefixed keys for `../new-shared/...`

This avoids breaking existing icon resolution and keeps imports deterministic.