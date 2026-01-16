---
name: test-model
description: Validate model correctness using MCP tools. Checks element references, relationships, view definitions, and syntax.
---

# Test LikeC4 Model

Use this skill when validating LikeC4 model correctness and integrity.

## Validation Workflow

### 1. Project Structure Validation (REQUIRED)

Use LikeC4 MCP `read-project-summary` to validate:
- All element kinds are defined in shared specifications
- All relationship kinds exist in spec files
- Tags are properly declared
- No orphaned elements

### 2. Element Reference Validation (REQUIRED)

Use LikeC4 MCP `search-element` to verify:
- All referenced elements exist
- FQN usage is correct for nested elements
- instanceOf references point to valid Containers

### 3. Relationship Validation (REQUIRED)

Use LikeC4 MCP `find-relationships` to check:
- Relationships use valid typed kinds
- No duplicate relationships between same elements
- All relationships have descriptive labels
- No reverse/return relationships exist

### 4. View Validation (RECOMMENDED)

Use LikeC4 MCP `open-view` to preview:
- Views render correctly without errors
- Include patterns show expected elements
- Layout hints (rank source/sink) work as intended
- No unexpected elements appear due to over-broad wildcards

### 5. Syntax Validation (RECOMMENDED)

Use Context7 MCP `query-docs` to verify:
- Relationship syntax is correct
- View syntax follows LikeC4 DSL standards
- Deployment instanceOf syntax is proper

## Common Issues to Check

### Broken References
```bash
# Use LikeC4 MCP search-element to find elements
# Verify all referenced elements exist in model
```

### Invalid Element Kinds
```bash
# Use LikeC4 MCP read-project-summary
# Check that all element kinds are in spec-*.c4 files
```

### Missing Relationship Labels
```likec4
❌ api -[calls]-> service          // Missing label
✅ api -[calls]-> service 'Fetches data'
```

### Over-broad View Includes
```likec4
❌ include **                      // Too broad
✅ include mySystem.*              // Scoped
```

## Testing Checklist

- [ ] Run LikeC4 MCP `read-project-summary` - verify all element kinds exist
- [ ] Search for all FQN references - use `search-element` to validate
- [ ] Check relationships - use `find-relationships` for key connections
- [ ] Preview all views - use `open-view` for each defined view
- [ ] Verify syntax - use Context7 MCP if uncertain about syntax features
- [ ] Check for compilation errors in VS Code Problems panel
- [ ] Run `likec4 start` locally to ensure diagrams render

## Output

Comprehensive validation report identifying:
- Broken or invalid references
- Syntax errors or warnings
- Missing or incorrect metadata
- Views that don't render as expected
