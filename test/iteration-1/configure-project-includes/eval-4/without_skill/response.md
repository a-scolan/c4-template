Keep this as an additive config change, not a replacement.

For `include.paths`, keep the current shared source and add the new one explicitly. If you want current behavior to remain stable, keep `../shared` before `../platform-shared`.

That order matters: resolution follows the order of `include.paths`, so changing the order can change which shared definition is found first.

Recommended approach:

- keep `../shared` first if existing shared definitions should keep winning
- add `../platform-shared` after it
- keep all paths relative to the project folder
- avoid absolute paths

For `imageAliases`, do not blindly merge colliding aliases under the same key. To avoid breaking current resolution:

- keep the existing shared alias unchanged, for example `"@": "../shared/images/"`
- add a second explicit alias for the new source, for example `"@platform": "../platform-shared/images/"`

If both sources currently define the same alias names, resolve that collision deliberately by using one of these strategies:

- prefix the new aliases
- rename the conflicting aliases
- document which source owns which alias namespace

The safest default is to preserve the existing `@` behavior and introduce a new prefixed alias for the new source, rather than letting one source silently override the other.