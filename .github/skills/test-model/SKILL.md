---
name: test-model
description: Use when validating model integrity—element references are valid, relationships are typed correctly, views render without errors, syntax is correct.
---

# Test LikeC4 Model

## Goal

Validate the model at the right depth.

Default to **quick validation** unless the prompt asks for a full audit.

## Modes

| Mode | Use when | Output |
|---|---|---|
| **Quick validation** | a narrow sanity check, a small edit, or a single suspicious file/view | short checklist + likely issues + next checks |
| **Full validation** | before commit, after structural changes, or when multiple files were touched | end-to-end validation report |

## When to Use

- Problems appear in the VS Code Problems panel
- Elements or relationships reference undefined kinds or FQNs
- Views render with unexpected elements or layout issues
- After structural changes (new elements, new topology, new deployment nodes)
- Before committing significant LikeC4 work

## Quick validation (default)

Run this small sequence first:

1. verify the active project and shared taxonomy
2. check the exact file(s) changed
3. verify FQNs and `instanceOf` targets
4. verify relationship kinds and technology placement
5. preview only the impacted view(s)

### Quick checklist

- [ ] kinds come from shared specs
- [ ] FQNs resolve to real elements
- [ ] `instanceOf` points to a real model container
- [ ] model relationships use `calls` / `async` / `reads` / `writes` / `uses`
- [ ] deployment relationships are used only for infrastructure-specific facts
- [ ] touched views still show the parent boundary and expected neighbors

## Full validation workflow

### 1. Project structure validation

Use `read-project-summary` to confirm:
- element kinds are declared
- relationship kinds are declared
- tags are valid
- the active project is the intended one

### 2. Reference validation

Use `search-element` or `read-element` to confirm:
- FQNs are correct
- nested references resolve
- `instanceOf` targets are real containers

### 3. Relationship validation

Use `find-relationships` to confirm:
- typed kinds are valid
- normal application traffic lives in the logical model
- no fake return path appears in async flows
- no duplicated app traffic is redrawn in deployment

### 4. View validation

Use `open-view` to confirm:
- the view renders without surprises
- include patterns are scoped correctly
- parent context is present
- rank hints, if any, are sparse and justified

### 5. Syntax/documentation validation

Use Context7 only if local files and specs still leave a syntax doubt.

## Parent-context validation

Every view must show what contains the focus.

- **C1**: system boundary and external context
- **C2**: parent system + containers + neighbors
- **C3**: parent container + components + neighbors
- **Deployment zone**: environment + zone + contained VMs
- **Deployment VM**: parent zone + VM + contained apps
- **Dynamic view**: initiating actor + causal sequence

### Typical failures

- ❌ C3 view without the parent container
- ❌ C2 view without the parent system
- ❌ deployment VM view without the parent zone
- ❌ dynamic view without the initiating actor

## Minimal issue patterns to check

### Missing relationship label

```likec4
❌ api -[calls]-> service
✅ api -[calls]-> service 'Fetches data'
```

### Over-broad include

```likec4
❌ include **
✅ include system.*
```

### Deployment protocol placed on the edge type in the logical model

```likec4
❌ webApp -[https]-> api
✅ webApp -[calls]-> api { technology 'HTTPS' }
```

## If MCP is unavailable

Do an offline validation pass:

1. read `projects/shared/SPEC_CHEATSHEET.md` and `projects/shared/spec-*.c4`
2. inspect the touched model/view/deployment files directly
3. inspect the Problems panel or compile errors available in the editor
4. provide the quick validation result first
5. list the MCP checks to run later (`read-project-summary`, `find-relationships`, `open-view`)

## Common mistakes

- ❌ expanding into a full workflow when the user only asked for a narrow sanity check
- ❌ checking syntax but not FQNs or `instanceOf`
- ❌ validating views without checking the parent boundary rule
- ❌ using deployment relationships to compensate for missing logical relationships
- ❌ ignoring the Problems panel because “the syntax looks fine”

## Output

Return either:
- a **quick validation** result with the highest-risk checks and immediate fixes, or
- a **full validation** report covering structure, references, relationships, and views
