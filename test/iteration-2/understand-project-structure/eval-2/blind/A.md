## Structured diagnosis for an unknown kind/relationship error

### 1. Check the source of truth first
Start with the files that define the taxonomy instead of guessing:
- Active project's `likec4.config.json`
- `projects/shared/spec-context.c4`
- `projects/shared/spec-containers.c4`
- `projects/shared/spec-components.c4`
- `projects/shared/spec-global.c4`
- `projects/shared/spec-deployment.c4` if the error is inside a deployment block
- The current project summary, if available, as the assembled view of the selected project

### 2. Compare the failing token against the valid taxonomy
First decide what the token is supposed to be.

#### If it is an element kind
Compare it against the exact names defined in the shared specs, for example:
- C1: `Actor_Person`, `System_Existing`, `System_External`
- C2: `Container_Api`, `Container_Webapp`, `Container_Database`, `Container_Queue`
- C3: `Component`
- Deployment: `Node_Environment`, `Zone_Vlan`, `Node_Vm`, `Infra_Fw`

#### If it is a relationship
Compare it against the exact relationship set for the file you are editing.
- **Model relationships** from `projects/shared/spec-global.c4`: `uses`, `calls`, `async`, `reads`, `writes`
- **Deployment relationships** from `projects/shared/spec-deployment.c4`: `http`, `https`, `tcp`, `nfs`, `amqp`, `oidc_saml`, `ldap`, `sql`, `redis`, `smtp`

### 3. Confirm exact spelling, case, and level
This workspace is sensitive to exact taxonomy names.
- Use **PascalCase** for kinds such as `Container_Api`
- Do not normalize names from memory
- Typical checks:
  - `Container_Api` vs `Container_API`
  - `Infra_Fw` vs `Infra_Firewall`
  - model relationship `calls` vs deployment relationship `https`

### 4. Confirmation sequence before correcting anything
1. Confirm the active project.
2. Confirm that the project's `likec4.config.json` includes the shared specs you expect.
3. Confirm whether the failing file is a **system model/view** file or a **deployment** file.
4. Compare the exact failing token against the spec definition files.
5. Cross-check with a known working example in the repository, such as:
   - `projects/template/system-model.c4`
   - `projects/spec-showcase/components.c4`
6. Only after that, rename the token or move the statement to the correct modeling level.

### 5. Fallback if the project summary looks inconsistent
Treat the summary as stale until proven otherwise.
- Re-read `likec4.config.json` and the shared spec files directly.
- Compare the failing token against a working repository example.
- Refresh the tool-generated project context before making the fix.
- If the file-level sources and the summary disagree, trust the file-level source of truth first.

### Bottom line
Diagnose in this order: **active project → included shared specs → model vs deployment level → exact taxonomy comparison → working example confirmation → correction**.
