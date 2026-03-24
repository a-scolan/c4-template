1. Probable error category: taxonomy + FQN.
2. Root cause: `Container_WebUi` is not a declared container kind in this workspace. The shared spec defines kinds such as `Container_Webapp`, `Container_Spa`, `Container_Browser`, and `Container_Api`. Separately, `api` is probably being referenced by short name instead of its full FQN, or the declared element name is different.
3. Verification step: check `projects/shared/SPEC_CHEATSHEET.md` for the exact container kinds, then inspect where the API element is declared and copy its full hierarchy path.
4. Minimal fix: replace `Container_WebUi` with the exact declared kind you mean, and reference the API by its full FQN.
Example:
`web = Container_Webapp 'Web UI'`
`web -[calls]-> corePlatform.api 'Calls API' { technology 'HTTPS' }`
If the UI is really a SPA, use `Container_Spa` instead.
