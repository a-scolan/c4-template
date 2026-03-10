# C4 Model Validation Checklist

Use this checklist to validate C4 models for completeness and quality.

Based on https://c4model.com/diagrams/checklist

## Validation Workflow

```
1. Syntax Validation → npx likec4 validate
2. Element Quality → Review descriptions, technologies
3. Relationship Quality → Check labels, directions
4. View Completeness → Verify titles, descriptions
5. C4 Checklist → Official diagram review
```

## Automated Validation

###Run LikeC4 CLI Validator

```bash
npx likec4 validate
```

**Checks:**
- ✓ Element references are valid
- ✓ Relationship endpoints exist
- ✓ View syntax is correct
- ✓ No duplicate element IDs
- ✓ Kind definitions match specification

## Element Quality Checklist

For each element:

- [ ] **Description present** - Explains purpose and responsibility
- [ ] **Technology documented** - For containers, components, nodes
- [ ] **Tags applied** - Using shared spec tags consistently
- [ ] **Icons set** - Where applicable (tech:, aws:, gcp:, azure:)
- [ ] **Links included** - To documentation, source code, dashboards (optional)
- [ ] **Metadata complete** - Team, owner, SLA (for system models, optional)

**Example:**

```likec4
api = Container_API 'REST API' {
  #backend #critical
  technology 'Node.js, Express'
  icon tech:nodejs
  
  description """
    Handles business logic and request routing
    
    **Responsibilities:**
    - API request validation
    - Business rule enforcement
    - Data access coordination
  """
  
  link https://docs.company.com/api 'API Documentation'
  
  metadata {
    team 'Backend'
    sla '99.9%'
  }
}
```

## Relationship Quality Checklist

For each relationship:

- [ ] **Label present** - Describes what the relationship does
- [ ] **Direction correct** - Arrow points in flow direction
- [ ] **Technology noted** - Protocol or communication method (if significant)
- [ ] **Relationship kind** - In arrow: `-[calls]->`, `-[async]->`, `-[reads]->`, `-[writes]->`
- [ ] **No return relationships** - Use one-way arrows only

**Example:**

```likec4
frontend -[calls]-> api 'Makes requests' {
  technology 'HTTPS'
}

api -[async]-> queue 'Publishes events' {
  technology 'AMQP'
}

api -[reads]-> database 'Queries data' {
  technology 'PostgreSQL'
}
```

## View Quality Checklist

For each view:

- [ ] **Title descriptive** - Clear what the view shows
- [ ] **Description present** - Explains scope and audience
- [ ] **Category folder** - In correct subfolder (C1, C2, C3, Use Cases, Deployment)
- [ ] **Parent context shown** - Views show surrounding/containing elements
- [ ] **Scope appropriate** - Not too broad (`include **`) or too narrow
- [ ] **Layout hints** - Rank source/sink where helpful (optional)
- [ ] **Links present** - To related documentation (optional)

**Example:**

```likec4
views 'C2' {
  view c2_containers {
    title 'Vault System Containers'
    
    description """
      Shows major containers and their interactions
      
      **Audience:** Architects and developers
      **Scope:** All containers within Vault system
    """
    
    include vault
    include vault.*
    
    link https://wiki.company.com/vault 'Vault Wiki'
    
    rank source { vault.api }
    rank sink { vault.database }
    
    autoLayout TopBottom
  }
}
```

## Official C4 Diagram Checklist

Source: https://c4model.com/diagrams/checklist

### General (All Diagrams)

- [ ] **Title present** - Clear, descriptive title
- [ ] **Diagram type stated** - C1, C2, C3, Deployment, Dynamic
- [ ] **Scope defined** - What does this diagram cover?
- [ ] **Key/Legend** - Colors, shapes, icons explained if used

### Elements (All Diagrams)

- [ ] **Names clear** - Meaningful element names
- [ ] **Types understood** - Actor, system, container, component clear
- [ ] **Purpose evident** - What each element does
- [ ] **Technology explicit** - Technologies documented where applicable
- [ ] **No undefined acronyms** - All abbreviations clear
- [ ] **Colors explained** - If different colors used, meaning is clear
- [ ] **Shapes explained** - Shape meanings documented
- [ ] **Icons identified** - Tech stack icons clear
- [ ] **Styling consistent** - Border, size, style used meaningfully

### Relationships (All Diagrams)

- [ ] **Labels describe intent** - What is relationship purpose?
- [ ] **Direction clear** - Arrows show correct direction
- [ ] **Technology documented** - Protocols, formats noted if significant
- [ ] **No undefined terms** - Communication methods clear
- [ ] **Colors meaningful** - If different line colors, explained
- [ ] **Arrow styles clear** - Solid vs dashed has meaning
- [ ] **Line styles meaningful** - Different styles indicate different types

## Model Completeness Checklist

### C1 Context

- [ ] System is defined with description
- [ ] All primary actors identified
- [ ] All external systems identified
- [ ] All major relationships documented
- [ ] External systems tagged #external
- [ ] One C1 Context view created
- [ ] View is static (no flows/sequences)

### C2 Containers

- [ ] System broken into logical deployable units
- [ ] Each container has clear purpose
- [ ] All technologies documented
- [ ] All major relationships between containers shown
- [ ] Synchronous vs asynchronous patterns clear
- [ ] One comprehensive C2 view exists
- [ ] Optional focused views for complex workflows

### C3 Components (Optional)

- [ ] Only complex/critical containers detailed
- [ ] Components are logical groupings, not classes
- [ ] Each C3 view shows parent container boundary
- [ ] Neighboring elements included for context
- [ ] Components are NOT separately deployable

### Deployment (Optional)

- [ ] Environments defined (Prod, Staging, Dev)
- [ ] Zones organized by tiers (DMZ, AppTier, DataTier)
- [ ] VMs have infrastructure specs (IP, CPU, RAM, ports)
- [ ] Zones have network details (VLANInstances use `instanceOf` to link to containers
- [ ] Deployment relationships mirror system model with protocols
- [ ] One deployment view per environment

### Dynamic (Optional)

- [ ] 2-5 use case flows documented (not every interaction)
- [ ] Each dynamic view starts with initiating actor
- [ ] Steps show temporal sequence
- [ ] Views placed in 'Use Cases' folder (not C1)
- [ ] Relationships labeled with action descriptions
- [ ] No parent-child relationships in dynamic views

## Consistency Checks

### Naming Consistency

- [ ] View IDs follow convention: `c1_name`, `c2_name`, `c3_name`
- [ ] Element kinds use PascalCase: `Container_API`, `Node_Vm`
- [ ] Variables use camelCase: `apiGateway`, `prodVm`
- [ ] Titles are descriptive: "Upload Service Internals"

### Terminology Consistency

- [ ] Same terms used throughout (not "API" vs "api" confusion)
- [ ] Relationship kinds consistent (calls, async, reads, writes)
- [ ] Tags consistent with shared spec
- [ ] No mix of container/component/service terminology

### Hierarchy Consistency

- [ ] Every C3 view has corresponding C2 container
- [ ] C3 view ID matches container name
- [ ] All containers appear in C2 view
- [ ] Deployment instances reference valid containers

## Validation Success Criteria

✅ **Pass automated** → `npx likec4 validate` returns no errors

✅ **Element quality** → All elements have:
- Description
- Technology (where applicable)
- Consistent naming

✅ **Relationship quality** → All relationships have:
- Descriptive labels
- Correct directions
- Technology/protocol (where significant)

✅ **View quality** → All views have:
- Title and description
- Correct category folder
- Parent context shown
- Appropriate scope

✅ **C4 checklist** → Official C4 review items all checked

✅ **Model completeness** → Required levels documented:
- C1 Context (always)
- C2 Containers (always)
- C3 Components (selective)
- Deployment (as needed)
- Dynamic (as needed)

## When Validation Fails

### Syntax Errors

**Fix:** Run `npx likec4 validate` to identify issues

Common syntax errors:
- Element reference not found → Use FQN: `mySystem.api`
- Unknown element kind → Check shared spec: `spec-containers.c4`
- Invalid relationship kind → Use valid kinds: `calls`, `async`, `reads`, `writes`
- Relationship type in block → Move to arrow: `-[calls]->`

### Element Quality Issues

**Fix:** Add missing metadata

- Missing description → Add: `description 'Purpose and responsibility'`
- No technology → Add: `technology 'Node.js, Express'`
- Missing icons → Add: `icon tech:nodejs`

### Relationship Issues

**Fix:** Improve relationship documentation

- Unlabeled → Add label: `api -> database 'Query data'`
- Wrong direction → Reverse arrow
- Missing technology → Add: `technology 'HTTPS'` in properties block

### View Issues

**Fix:** Complete view metadata

- No title → Add: `title 'System Context'`
- No description → Add: `description 'Shows...'`
- Over-broad includes → Change `include **` to `include system.*`
- Missing context → Add parent element include

### C4 Checklist Issues

**Fix:** Review against official checklist

- Generic names → Use descriptive names: "Upload Service" not "Service1"
- No legend → Add key explaining colors, shapes, icons
- Unclear relationships → Add technology and direction labels
- Missing scope → Add description explaining what view shows

## Validation Tools

### Manual Review

Use these skills for specific checks:

- `test-model` - Comprehensive validation workflow
- `create-element` - Element quality standards
- `create-relationship` - Relationship documentation standards
- `design-view` - View organization and context requirements

### Automated Tools

```bash
# Validate syntax and references
npx likec4 validate

# Check specific directory
npx likec4 validate ./my-architecture

# Validate without layout checks
npx likec4 validate --ignore-layout
```

### MCP Tools

Use LikeC4 MCP for validation:

```javascript
// Check element exists
mcp_likec4_read_element({ id: 'mySystem.api', project: 'default' })

// Verify relationships
mcp_likec4_find_relationships({ element1: 'mySystem.api', element2: 'mySystem.database' })

// Validate view
mcp_likec4_read_view({ viewId: 'c2_containers', project: 'default' })

// Check project structure
mcp_likec4_read_project_summary({ project: 'default' })
```

## Continuous Validation

### Pre-Commit

Add validation to Git hooks:

```bash
#!/bin/bash
# .git/hooks/pre-commit

npx likec4 validate || {
  echo "LikeC4 validation failed! Fix errors before committing."
  exit 1
}
```

### CI/CD

Add to pipeline:

```yaml
# .github/workflows/validate.yml
- name: Validate LikeC4 models
  run: npx likec4 validate
```

### Regular Review

Schedule periodic reviews:

- Weekly: Run validation on main branch
- Sprint end: Review against C4 checklist
- Major changes: Full quality review

## Resources

- **C4 Checklist:** https://c4model.com/diagrams/checklist
- **LikeC4 Validation:** `npx likec4 validate --help`
- **Test Model Skill:** Use `test-model` skill for detailed workflow
