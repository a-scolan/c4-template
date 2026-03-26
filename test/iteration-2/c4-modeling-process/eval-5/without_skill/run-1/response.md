Follow this order without skipping:

1. **Re-sync workspace and shared specifications**
   - Re-read shared constraints and multi-project boundaries after spec changes.
2. **Re-validate impacted model parts**
   - Confirm existing elements/relationships still align with updated shared specs.
3. **Prepare the sensitive C3 scope**
   - Define exact audience and filtering (only necessary internals).
4. **Build/update C3 elements and relations**
   - Add only required internals; keep naming and semantics consistent.
5. **Design and harden the sensitive C3 view**
   - Apply view scoping/customization to avoid overexposure.
6. **Then document the nominal user scenario**
   - Create a dynamic/sequence view for the nominal flow.
7. **Final consistency pass across projects**
   - Ensure shared-spec compliance and cross-project coherence.

Skills handoff sequence:

- `sync-with-template` + `organize-multi-project` (after shared-spec changes)
- `create-element` / `create-relationship` (if C3 internals are missing)
- `design-view` + `customize-view` (for the sensitive C3 view)
- `create-sequence-view` (for the nominal scenario)
- `test-model` and `troubleshoot-errors` (final validation/fix pass)