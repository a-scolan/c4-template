Use a **model relationship** between the two containers:

`webApp -[calls]-> api "Requests API" { technology "HTTPS" }`

Rule of thumb:
- The **relationship instance** goes in your system model (where `webApp` and `api` are declared).
- The **relationship type definition** (`calls`, `reads`, `writes`, `async`, etc.) belongs in `specification { relationship ... }` (for this workspace, that is in shared spec files such as `projects/shared/spec-global.c4`).
