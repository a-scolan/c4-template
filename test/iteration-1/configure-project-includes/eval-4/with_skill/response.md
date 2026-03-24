Keep the current shared include and alias stable, then add the new source beside it:
- `include.paths` should become `["../shared", "../platform-shared"]`.
- Leave the existing shared alias unchanged, for example `"@": "../shared/images/"`, so all current icon references keep working.
- Do not repoint `"@"` at `../platform-shared/images/` if that would change existing resolution.
- If the platform source needs its own icons, give it a separate alias such as `"@platform": "../platform-shared/images/"` instead of redefining `"@"`.

That preserves current behavior and avoids alias collisions.
