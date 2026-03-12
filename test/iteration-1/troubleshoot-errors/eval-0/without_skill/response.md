These are two separate root causes, so diagnose them independently.

1. **Verify the kind first**
   - `Container_WebUi` is not one of the declared container kinds in the shared specs.
   - In this workspace, the valid web UI container kind is `Container_Webapp`.
   - So the first error is a bad kind name, most likely a typo or a guessed kind.

2. **Verify the element id separately**
   - `api` is defined as a child of `mySystem`, so its full name is `mySystem.api`.
   - If the failing reference is written outside the `mySystem` scope, `api` alone will not resolve.
   - That makes `Element not found: api` a naming/scope problem, not a kind problem.

3. **Diagnose in the right order**
   - Check the declared kinds first.
   - Then inspect the actual element hierarchy and confirm the exact ids that exist.
   - Only after that should you rename anything.

4. **Targeted fix**
   - Replace `Container_WebUi` with `Container_Webapp`.
   - Replace out-of-scope references to `api` with `mySystem.api`.

So the real diagnosis is **both** an invalid kind and an incorrect FQN reference.