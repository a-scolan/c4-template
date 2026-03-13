Full preflight before adding a new API container:
1. Active project first: this workspace has two visible LikeC4 project roots, `projects/template` (`name: template-project`) and `projects/spec-showcase` (`name: spec-showcase`). Before any change, fix one `likec4.config.json` as the active project and keep model + views inside that folder only. Both projects include `../shared`, so the shared taxonomy comes from `projects/shared/`.
2. Available taxonomy from shared specs:
- C1 kinds: `Actor_Person`, `Actor_Staff`, `Actor_Admin`, `System_New`, `System_Existing`, `System_Legacy`, `System_External`
- C2 kinds: `Container_Api`, `Container_Api_Geo`, `Container_Queue`, `Container_Webapp`, `Container_WebServer`, `Container_ApplicationServer`, `Container_ProcessingServer`, `Container_ExchangeServer`, `Container_IamServer`, `Container_Database`, `Container_DatabaseGeo`, `Container_ObjectStorage`, `Container_Directory`, `Container_DataServer`, `Container_FileServer`, `Container_ReverseProxy`, `Container_Waf`, `Container_Loadbalancer`, `Container_Browser`, `Container_MobileApp`, `Container_Spa`
- C3 kind: `Component`
- Model relationships: `uses`, `calls`, `async`, `reads`, `writes`
- Deployment-only relationships: `http`, `https`, `tcp`, `nfs`, `amqp`, `oidc_saml`, `ldap`, `sql`, `redis`, `smtp`
- Core tags: `#Internal`, `#External`, `#Legacy`, `#Cloud`, `#Saas`, `#Queue`, `#Security`, plus family/type tags from the shared spec files such as `#Actor`, `#System`, `#Container`, `#Component`, `#Api`, `#Database`, `#ObjectStorage`, and deployment tags in `spec-deployment.c4`.
3. Source-of-truth files:
- Project activation/boundary: active project's `likec4.config.json`
- Taxonomy: `projects/shared/spec-context.c4`, `spec-containers.c4`, `spec-components.c4`, `spec-global.c4`, `spec-deployment.c4`
- Local model/view truth: the active project's own model and view files. In `projects/template`, that is `system-model.c4` and `system-views.c4`; in the showcase-style split, it is files such as `containers.c4` / `container-views.c4` and `components.c4` / `component-views.c4`.
- Important repo rule from `README.md`: `projects/shared/` is the automation-facing source of truth; `projects/spec-showcase/` and `projects/template/` are examples, not the authoritative taxonomy.
4. C1 -> C2 -> C3 plan:
- C1: lock the owning system and its actors/external dependencies first. If the system boundary is unclear, resolve that before adding a container.
- C2: add the new `Container_Api` inside the owning system, set `technology`/`description`, then add the right `calls` / `reads` / `writes` / `async` relationships. If the API introduces async work, add `Container_Queue` at the same time.
- C3: only after the C2 role is stable, add internal `Component` children inside that API container and create or update a C3 view `of` that container.
One practical warning: prefer the exact names from `projects/shared/spec-*.c4`, not aliases from summaries. The cheat sheet already drifts from source of truth in places.
