---
name: troubleshoot-errors
description: Diagnose common LikeC4 errors (element not found, unknown kinds, invalid relationships). Provides causes and solutions.
---

# Troubleshoot LikeC4 Errors

Use this skill when resolving common LikeC4 syntax or reference errors.

## Common Issues

### "Element not found"
- **Cause:** Using short name instead of FQN
- **Solution:** Use `mySystem.api` not `api` for nested elements

### "Unknown element kind"
- **Cause:** Invalid or generic element kind
- **Solution:** Check `projects/shared/spec-*.c4` for valid kinds; use specific kinds like `Container_Api` not `Container`

### "Invalid relationship kind"
- **Cause:** Undefined relationship type
- **Solution:** Use defined kinds: `calls`, `async`, `reads`, `writes`, `uses` (model) or `http`, `https`, `tcp` (deployment)

### Relationship syntax error (calls/uses/reads/writes in block)
- **Error:** `calls 'Action description'` inside relationship block
- **Cause:** Relationship kind placed in property block instead of arrow
- **Solution:** Move type to arrow: `source -[calls]-> target 'Action' { technology 'X' }`
- **Example fix:**
  ```likec4
  // ❌ WRONG
  api -> service {
    calls 'Fetch data'
  }
  
  // ✅ CORRECT
  api -[calls]-> service 'Fetch data'
  ```

### Parent-child relationship in dynamic view
- **Error:** Compilation error when showing `container -> container.component` in dynamic view
- **Cause:** Dynamic views cannot show parent calling its own child (conceptual violation)
- **Solution:** Have actor/external element directly access the component
- **Example fix:**
  ```likec4
  // ❌ WRONG (in dynamic view)
  user -> system.webapp
  system.webapp -> system.webapp.authModule
  
  // ✅ CORRECT
  user -> system.webapp.authModule 'Accesses directly'
  system.webapp.authModule -> ldapServer 'Validates'
  ```

### Invalid "rank same" constraint
- **Error:** `rank same` rule fails with elements from different parent contexts
- **Cause:** Rank constraints can only group elements sharing the same parent
- **Solution:** Remove or split constraint, only rank siblings together
- **Example fix:**
  ```likec4
  // ❌ WRONG: Different parents (external vs internal)
  rank same ldapServer, devforge.postgresDb
  
  // ✅ CORRECT: Same parent context
  rank same devforge.api, devforge.database
  ```

### Diagram shows unexpected elements
- **Cause:** Over-broad wildcard includes like `include **`
- **Solution:** Use scoped wildcards: `include mySystem.*` or `include mySystem.* ->`

### "instanceOf target not found"
- **Cause:** Referencing non-existent or wrong element type
- **Solution:** Ensure target is a Container from model, use FQN: `instanceOf mySystem.api`
