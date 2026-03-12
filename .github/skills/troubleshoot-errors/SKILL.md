---
name: troubleshoot-errors
description: Use when resolving LikeC4 errors—element not found, unknown kinds, invalid relationships, type mismatches, syntax failures. Provides root causes and fixes.
---

# Troubleshoot LikeC4 Errors

## Goal

Diagnose the root cause, verify it quickly, then show the smallest correct fix.

Default response shape:
1. **probable error category**
2. **root cause**
3. **verification step**
4. **minimal fix**

Prefer one corrected snippet over a long essay.

## When to Use

- Errors appear in the VS Code Problems panel
- LikeC4 reports unknown kinds, unknown relationships, or missing elements
- Views render incorrectly or show unexpected elements
- Syntax errors appear after editing model/view/deployment files

## Triage order

1. identify whether the problem is taxonomy, FQN, syntax, view scope, or deployment inheritance
2. compare the failing construct against shared specs and the project summary
3. verify the smallest relevant file/line
4. apply the minimal correction instead of compensating elsewhere

## Quick reference

| Symptom | Root cause | Minimal fix |
|---|---|---|
| `Element not found` | short name instead of FQN | use full FQN such as `system.api` |
| `Unknown kind` | undeclared element kind | replace with exact shared kind from `spec-*.c4` |
| `Invalid relationship kind` | undeclared or wrong-scope relationship type | use model kinds (`calls`, `async`, `reads`, `writes`, `uses`) or proper deployment kinds |
| `Unknown relationship type: https` in `model {}` | deployment type used in logical model | use `-[calls]->` + `technology 'HTTPS'` |
| syntax error in relationship block | kind placed in properties block | move the kind into the arrow |
| dynamic view parent → child | containment shown as interaction | have the actor or peer call the component directly |
| unexpected elements in view | include pattern too broad | scope includes to the intended boundary |
| `instanceOf target not found` | wrong FQN or wrong target type | point `instanceOf` to a real model container FQN |
| duplicate app edges in deployment | logical traffic restated in deployment | remove duplicate deployment edges and rely on inherited model relationships |

## Minimal fix templates

### 1. Unknown kind

- **Root cause:** the element kind is not declared in shared specs
- **Verify:** check `projects/shared/spec-*.c4` or the project summary
- **Fix:** replace guessed kinds with exact shared ones

```likec4
// ❌ Wrong
api = Container_API 'API'

// ✅ Correct
api = Container_Api 'API' {
  technology 'Node.js'
  description 'Exposes the platform API.'
}
```

### 2. Wrong FQN / element not found

- **Root cause:** nested element referenced by short name only
- **Verify:** inspect parent hierarchy or use `search-element`
- **Fix:** use the full FQN

```likec4
// ❌ Wrong
instanceOf api

// ✅ Correct
instanceOf corePlatform.api
```

### 3. Deployment relationship kind used in `model {}`

- **Root cause:** protocol encoded as relationship type instead of `technology`
- **Verify:** confirm you are in the logical model, not deployment
- **Fix:** keep the model relationship kind and move the protocol to `technology`

```likec4
// ❌ Wrong
webApp -[https]-> api 'Makes API requests'

// ✅ Correct
webApp -[calls]-> api 'Makes API requests' {
  technology 'HTTPS'
}
```

### 4. Relationship kind inside block

- **Root cause:** `calls`, `reads`, or similar placed in the property block
- **Verify:** inspect the exact arrow syntax
- **Fix:** move the kind into the arrow

```likec4
// ❌ Wrong
api -> service {
  calls 'Fetch data'
}

// ✅ Correct
api -[calls]-> service 'Fetch data'
```

### 5. Dynamic view parent → child error

- **Root cause:** a container is shown calling its own component in a dynamic view
- **Verify:** check whether both endpoints are in a containment chain
- **Fix:** have the actor or an external peer target the child directly

```likec4
// ❌ Wrong
user -> system.webApp
system.webApp -> system.webApp.authModule

// ✅ Correct
user -> system.webApp.authModule 'Starts login'
system.webApp.authModule -> directoryService 'Validates credentials'
```

### 6. Duplicate deployment edges

- **Root cause:** normal application traffic was redrawn between deployment instances
- **Verify:** check whether the corresponding model relationship already exists
- **Fix:** keep the relationship in `model {}` and let `instanceOf` propagate it

```likec4
// ❌ Wrong
Prod.Web.webApp -[https]-> Prod.App.apiApp 'Browser traffic'

// ✅ Better
webApp -[calls]-> api 'Browser traffic' {
  technology 'HTTPS'
}
```

## View/layout-specific fixes

### Invalid `rank same`

Only rank siblings that share the same parent context.

```likec4
// ❌ Wrong
rank same ldapServer, devforge.postgresDb

// ✅ Correct
rank same devforge.api, devforge.database
```

### Too many rank hints

- **Root cause:** the view is over-constrained
- **Fix:** remove most `rank` hints, keep `autoLayout`, then add at most one obvious anchor if still needed

### Over-broad include

```likec4
// ❌ Wrong
include **

// ✅ Better
include corePlatform.*
include -> corePlatform.api
include corePlatform.api ->
```

## If MCP is unavailable

Use an offline diagnosis path:

1. inspect the exact failing line and file type (`model`, `view`, or deployment)
2. compare it to `projects/shared/SPEC_CHEATSHEET.md` and `projects/shared/spec-*.c4`
3. inspect nearby FQNs and hierarchy in the local model files
4. give the minimal corrected snippet now
5. list the MCP checks to run later (`read-project-summary`, `find-relationships`, `search-element`)

## Common mistakes

- ❌ fixing the symptom without identifying the category of error first
- ❌ guessing kinds instead of comparing against shared specs
- ❌ working around a bad model with broader view includes
- ❌ using deployment relationship kinds in `model {}`
- ❌ redrawing inherited app traffic in deployment

## Output

Return a short diagnosis with the root cause, the verification step, and a corrected snippet ready to paste.
