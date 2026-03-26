1. **Probable error category**
   - Dynamic-view containment misuse + invalid layout constraint.

2. **Root cause**
   - `system -> system.api` models parent-to-child containment as interaction (invalid in this context).
   - `rank same user, system.api` tries to rank elements that are not siblings under the same parent scope.

3. **Verification step**
   - Check whether source/target are in a parent-child chain; if yes, do not model it as an interaction step.
   - Ensure every `rank same` group contains only siblings.

4. **Minimal fix**

```likec4
dynamic userLogin {
  user -> system.api 'Calls API directly'
  system.api -> system.authService 'Validates credentials'

  // Keep rank hints only for siblings (or remove if unsure)
  // rank same user, admin
}
```