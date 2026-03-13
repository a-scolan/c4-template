Preflight before adding a new API container:
1. Confirm the active project first. Do not assume it. In this repo, the visible project configs are `projects/template/likec4.config.json` (`name: template-project`) and `projects/spec-showcase/likec4.config.json` (`name: spec-showcase`). Reliable method: run `list-projects`, then `read-project-summary` for the intended project; offline, verify the matching `projects/<project>/likec4.config.json`.
2. Lock the semantic source of truth in this order: project summary, `projects/shared/SPEC_CHEATSHEET.md` for orientation, then the actual declarations in `projects/shared/spec-context.c4`, `spec-containers.c4`, `spec-components.c4`, `spec-global.c4`, and `spec-deployment.c4`.
3. Check project wiring: confirm the chosen project includes `../shared`, then inspect the nearby model/view files that will actually be edited.
4. Valid local taxonomy already present includes kinds such as `Actor_Person`, `System_Existing`, `System_External`, `Container_Api`, `Container_Queue`, `Container_Database`, and `Component`; tags such as `#Internal`, `#External`, `#Legacy`, `#Cloud`, `#Saas`, `#Queue`, and `#Security`; model relationships `uses`, `calls`, `async`, `reads`, `writes`; and deployment relationships `http`, `https`, `tcp`, `nfs`, `amqp`, `ldap`, `sql`, `redis`, `smtp`, `oidc_saml`.
5. Risks avoided by this preflight: wrong project, stale taxonomy, invalid kind/relationship names, wrong parent system/container, and mixing deployment protocols into the system model.
Ordered C1 -> C2 -> C3 plan:
- C1: confirm the target system boundary and any external actors/systems first.
- C2: add the new `Container_Api` under the correct system and wire only valid model relationships (`calls`, `async`, `reads`, `writes`, `uses`) with technology on the relationship.
- C3: only if deeper internal detail is needed, confirm the real parent API container and then model components under it and update the C3 view.
Treat shared specs and the project summary as primary truth; example projects are references only. After this preflight, the sequencing handoff belongs to `c4-modeling-process`.
