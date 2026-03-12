Do not jump straight to the sensitive C3 view. Revalidate the workspace first.

1. **Reconfirm the active project and shared specifications**
   - This workspace is multi-project, and project configs include `../shared`.
   - If shared specs changed, verify the active project still uses the right kinds, tags, naming, and conventions before editing detailed views.

2. **Recheck the C1 understanding**
   - Make sure the system boundary, actors, and external systems are still correct.

3. **Recheck the C2 structure**
   - Confirm the container model still matches the current architecture after the shared-spec changes.
   - Fix structural inconsistencies before going deeper.

4. **Create the C3 view selectively**
   - Add the detailed C3 only for the sensitive or complex container that truly needs it.
   - Keep the scope tight and consistent with the C2 story.

5. **After the static structure is stable, document the nominal user scenario**
   - Put the scenario in a **dynamic / use-case view**, because it is time-ordered behavior rather than static structure.

6. **Finish with a full consistency check**
   - Review affected projects and views to ensure the shared-spec changes did not introduce mismatches.

So the order is: **shared context → C1 → C2 → C3 (selective) → dynamic scenario → final verification**.