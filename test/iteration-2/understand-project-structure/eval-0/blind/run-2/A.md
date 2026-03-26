Before editing, run this preflight in order:

1. Confirm active project (do not assume).
2. Re-read project summary for that project.
3. Validate taxonomy from shared specs:
   - `projects/shared/SPEC_CHEATSHEET.md`
   - `projects/shared/spec-context.c4`
   - `projects/shared/spec-containers.c4`
   - `projects/shared/spec-components.c4`
   - `projects/shared/spec-deployment.c4`
4. Verify project wiring (`likec4.config.json` includes) for the target project.
5. Only then edit model/view files.

Available local taxonomy examples (from shared specs):

- Element kinds: `System_External`, `Container_Api`, `Container_Queue`, `Container_Database`, `Component`
- Deployment node kinds: `Node_Environment`, `Zone_Vlan`, `Node_Vm`, `Node_App`
- Model relationships: `uses`, `calls`, `async`, `reads`, `writes`
- Deployment relationships: `http`, `https`, `tcp`, `amqp`, `ldap`, `sql`, `redis`, `smtp`
- Common tags: `#System`, `#Container`, `#Api`, `#Queue`, `#Database`, `#Production`, `#AppTier`, `#DataTier`

Risks this preflight avoids:

- Wrong project context after switching
- Unknown kind/relationship from guessing taxonomy
- Wrong C3 parent chain / invalid FQN
- Treating examples as canonical taxonomy

C1 → C2 → C3 plan for adding a new API container:

- C1: confirm actor/system boundaries and external systems around the target system.
- C2: add `Container_Api` in the correct parent system, then wire `calls/async/reads/writes` as needed.
- C3: only if necessary, decompose that API into `Component` elements and internal calls.

Handoff: once preflight is complete, use `c4-modeling-process` to sequence C1→C2→C3 execution safely.