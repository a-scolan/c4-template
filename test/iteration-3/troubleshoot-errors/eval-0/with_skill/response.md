1. probable error category: taxonomy error plus FQN resolution error.
2. root cause: `Container_WebUi` is not a declared container kind in this workspace. The shared specs define kinds such as `Container_Webapp`, `Container_WebServer`, `Container_Spa`, and `Container_Api`, so `Container_WebUi` is a guessed name, not a valid one. Separately, `api` is too ambiguous as written and likely needs the real fully qualified name, for example `system.api`.
3. verification step: the right first move is to check the project summary (`read-project-summary` if available) before renaming anything blindly. With MCP unavailable, compare against `projects/shared/spec-containers.c4` / `projects/shared/SPEC_CHEATSHEET.md`, then inspect the model hierarchy to find the API container’s actual parent path.
4. minimal fix: replace the invalid kind with the exact declared one, then reference the API by its real FQN.

Example:
`web = Container_Webapp 'Web UI'`
`web -[calls]-> mySystem.api 'Calls API' { technology 'HTTPS' }`
