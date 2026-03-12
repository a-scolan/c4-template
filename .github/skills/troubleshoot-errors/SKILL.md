---
name: troubleshoot-errors
description: Use when resolving LikeC4 errors—element not found, unknown kinds, invalid relationships, type mismatches, syntax failures. Provides root causes and fixes.
---

# Troubleshoot LikeC4 Errors

## Overview

Diagnoses and resolves common LikeC4 compilation and rendering errors by mapping symptoms to root causes and targeted fixes.

## When to Use

- Compilation errors appear in VS Code Problems panel
- LikeC4 MCP returns "element not found" or "unknown kind" responses
- Diagram rendering fails or shows unexpected elements
- Syntax errors after editing model or view files

**Tip:** Use `read-project-summary` first to confirm valid element kinds, tags, and relationship types.

## Quick Reference

| Symptom | Root Cause | Fix |
|---------|-----------|-----|
| "Element not found" | Short name instead of FQN | Use a full FQN such as `system.api`, not `api` |
| "Unknown kind" | Invalid element kind | Check `projects/shared/spec-*.c4` |
| "Invalid relationship kind" | Undefined relationship type | Use `calls`, `async`, `reads`, `writes` |
| `Unknown relationship type: https` in `model {}` | Deployment kind used in system model | Use a model kind plus `technology 'HTTPS'` |
| Syntax error in relationship block | Kind in property block | Move type to arrow: `-[calls]->` |
| Parent-child in dynamic view | Conceptual violation | Have actor access component directly |
| Unexpected elements in diagram | Over-broad wildcard include | Scope: `include system.*` |
| "instanceOf target not found" | Wrong element type or FQN | Target must be a Container, use a full FQN |
| Deployment diagram shows duplicate app edges | Relationship restated in deployment | Remove duplicate edge and rely on inherited model relationship |

## Common Issues

### "Element not found"
- **Cause:** Using short name instead of FQN
- **Solution:** Use a full FQN like `system.api`, not `api`, for nested elements

### "Unknown element kind"
- **Cause:** Invalid or generic element kind
- **Solution:** Check `projects/shared/spec-*.c4` for valid kinds; use specific kinds like `Container_Api` not `Container`

### "Invalid relationship kind"
- **Cause:** Undefined relationship type
- **Solution:** Use defined kinds: `calls`, `async`, `reads`, `writes`, `uses` (model) or `http`, `https`, `tcp` (deployment)

### `Unknown relationship type: https` (or `ldap`, `amqp`, etc.) inside `model {}`
- **Cause:** A deployment relationship kind was used in the logical system model.
- **Solution:** Keep a model relationship kind in the arrow and move the protocol to the relationship technology.
- **Example fix:**
  ```likec4
  // ❌ WRONG
  webapp -[https]-> api 'Makes API requests'

  // ✅ CORRECT
  webapp -[calls]-> api 'Makes API requests' {
    technology 'HTTPS'
  }
  ```

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

### View became brittle after adding many rank hints
- **Symptom:** Layout looks worse or starts breaking after adding several `rank source`, `rank sink`, or `rank same` directives
- **Cause:** The view is over-constrained; rank hints are being used to force structure that should come from `autoLayout` and better includes
- **Solution:** Remove most rank hints, keep `autoLayout`, then reintroduce at most one or two obvious anchors if still needed (often just the initiating user as `rank source`)

### Diagram shows unexpected elements
- **Cause:** Over-broad wildcard includes like `include **`
- **Solution:** Use scoped wildcards: `include system.*` or `include system.* ->`

### "instanceOf target not found"
- **Cause:** Referencing non-existent or wrong element type
- **Solution:** Ensure target is a Container from model and use a full FQN such as `instanceOf system.api`

### Deployment view is cluttered with duplicate relationships
- **Cause:** Application traffic was restated in deployment nodes/views instead of being inherited from the system model.
- **Solution:** Delete the duplicate deployment relationships, add or fix the logical relationship in `model {}`, and put protocol/port details on that relationship’s `technology` field.

## Common Mistakes

- ❌ Fixing the symptom (renaming) without finding the root cause (wrong FQN or kind)
- ❌ Using generic kinds (`Container`) instead of spec-defined kinds (`Container_Api`)
- ❌ Retrying the same syntax without checking Context7 MCP for current DSL docs
- ❌ Editing view includes to work around a model error instead of fixing the model
- ❌ Using deployment relationship kinds in `model {}` instead of `technology 'HTTPS'` / `technology 'AMQP'` / `technology 'Manual'`
- ❌ Recreating inherited app-level relationships in deployment just to show technical details
- ❌ Skipping `read-project-summary` — always verify valid kinds before manual edits
