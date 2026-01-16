# LikeC4 Project Template

A minimal, ready-to-use template for creating new LikeC4 architecture documentation projects with GitHub Copilot support and git subtree integration for shared specifications.

---

## Initial Setup

### 1. Enable GitHub Copilot Skills (Recommended)

Set this in VS Code `.vscode/settings.json` to unlock 14 built-in architecture skills:

```json
{
  "github.copilot.chat.useAgentSkills": true
}
```

Once enabled, ask Copilot: "What skills are available?", "Use the create-element skill", or "Help me troubleshoot this error"

**14 available skills:** understand-project-structure, create-element, create-relationship, create-sequence-view, model-deployment, design-view, customize-view, configure-project-includes, organize-multi-project, implement-pattern, test-model, troubleshoot-errors, document-decision, lookup-element-kinds

### 2. Copy the Template

For a single project:

```bash
cp -r projects/template projects/my-new-project
cd projects/my-new-project
```

### 3. (Optional) Add as Git Subtree to Existing Project

If integrating into an existing architecture repository:

```bash
# Add c4-template as remote
git remote add c4-template https://github.com/a-scolan/c4-template.git

# Pull three subtrees with squashed history
git subtree add --prefix=.github c4-template main --squash
git subtree add --prefix=projects/shared c4-template main --squash
git subtree add --prefix=projects/spec-showcase c4-template main --squash
```

---

## Quick Start

### Configure Your Project

Edit `likec4.config.json`:

```json
{
  "name": "my-new-project",           // ⚠️ Change to unique project identifier
  "title": "My Project Title",         // ⚠️ Change to descriptive title
  "include": {
    "paths": ["../shared"]             // ✅ Keep this to use shared specs
  },
  "imageAliases": {
    "@": "../shared/images"            // ✅ Keep this for shared icons
  }
}
```

### Update the Model

Edit `system-model.c4`:

- Replace `mySystem` with your system name
- Add actors (users, external systems)
- Define containers (applications, databases, services)
- Create relationships with typed kinds

### Customize Views

Edit `system-views.c4`:

- Update view titles and descriptions
- Adjust `include` statements for relevant elements
- Use `rank` to control layout

### Preview Diagrams

```bash
# From workspace root
npx likec4 start

# Open http://localhost:3000
```

---

## File Structure

| File | Purpose | Required |
|------|---------|----------|
| `likec4.config.json` | Project configuration | ✅ Yes |
| `system-model.c4` | Logical architecture | ✅ Yes |
| `system-views.c4` | Visualization definitions | ✅ Yes |

### Optional Files

- **`system-sequences.c4`** - Dynamic views / use case flows
- **`deployment.c4`** - Physical infrastructure (environments, VMs, networks)
- **`deployment-views.c4`** - Infrastructure topology views

---

## Best Practices

### Element Naming

✅ **Use PascalCase with Category_Subtype:**

```likec4
Actor_Person           // ✅ Correct
System_Existing        // ✅ Correct
Container_Api          // ✅ Correct

actor_person           // ❌ Wrong (lowercase)
ActorPerson            // ❌ Wrong (no separator)
```

### Typed Relationships

✅ **All relationships MUST have explicit kinds:**

```likec4
api -[calls]-> service 'Invokes'         // ✅ Correct
api -[reads]-> database 'Queries'        // ✅ Correct
worker -[async]-> queue 'Consumes'       // ✅ Correct
api -[writes]-> storage 'Saves to'       // ✅ Correct

api -> service 'Invokes'                 // ❌ Wrong (no kind)
```

### Descriptions and Technology

✅ **Always include:**

```likec4
api = Container_Api 'API Server' {
  technology 'Node.js, Express'          // ✅ Required
  description 'Handles business logic'   // ✅ Required
}
```

### View Patterns

✅ **Use scoped wildcards:**

```likec4
view c2_containers {
  include mySystem.*                     // ✅ All containers
  include mySystem.* -> *                // ✅ Outgoing relationships
  include * -> mySystem.*                // ✅ Incoming relationships
  
  include ** -> **                       // ❌ Too broad
}
```

✅ **Use rank for layout:**

```likec4
view c1_context {
  include user, mySystem, emailService
  
  rank source { user }                   // Top
  rank sink { emailService }             // Bottom
}
```

### No Return Relationships

❌ **Don't create implicit returns:**

```likec4
client -[calls]-> server 'Requests'     // ✅ Correct

// ❌ Don't add:
server -[calls]-> client 'Responds'
```

---

## Element Kinds Reference

### Actors (C1)
- `Actor_Person`, `Actor_Staff`, `Actor_Admin`

### Systems (C1)
- `System_Existing`, `System_New`, `System_Legacy`, `System_External`

### Containers (C2)
- `Container_Api`, `Container_Webapp`, `Container_Database`, `Container_Queue`, `Container_Cache`, `Container_WebServer`, `Container_LoadBalancer`, `Container_Storage`
- And 20+ more in `projects/shared/spec-containers.c4`

### Relationship Kinds
**Model:** `calls`, `async`, `reads`, `writes`, `uses`
**Deployment:** `http`, `https`, `tcp`, `nfs`, `amqp`, `sql`, `redis`

Complete reference: `projects/shared/SPEC_CHEATSHEET.md`

---

## Common Workflows

### 1. Document a New System

1. Define system boundary in `system-model.c4`
2. Add actors
3. Define containers
4. Add typed relationships
5. Create C1 and C2 views

### 2. Add External Dependency

```likec4
externalService = System_External 'Payment Gateway' {
  technology 'Stripe API'
  description 'Handles payment processing'
  #External
}

mySystem.api -[calls]-> externalService 'Process payments'
```

### 3. Model Async Communication

```likec4
queue = Container_Queue 'Message Queue' {
  technology 'RabbitMQ'
  description 'Async job processing'
}

api -[async]-> queue 'Publishes jobs'
worker -[async]-> queue 'Consumes jobs'
```

### 4. Add Component (C3) Views

```likec4
api = Container_Api 'API Server' {
  technology 'Node.js'
  
  router = Component 'Router' {
    technology 'Express Router'
    description 'Routes HTTP requests'
  }
}

view c3_api_components {
  title 'C3 / API Components'
  include user, mySystem.api.*, mySystem.database
}
```

---

## Using as Git Subtree

### Periodic Synchronization

Pull updates quarterly or when specifications change:

```bash
# Fetch latest
git fetch c4-template main

# Pull updates for each subtree (--squash keeps history clean)
git subtree pull --prefix=.github c4-template main --squash
git subtree pull --prefix=projects/shared c4-template main --squash
git subtree pull --prefix=projects/spec-showcase c4-template main --squash

# Review and push
git push
```

**Note:** The `--squash` flag consolidates all c4-template changes into a single commit per sync. Updates are manual—subtrees do not auto-sync.

### What Gets Included

When cloning a repository with git subtrees, all content appears automatically:

- Shared specifications and examples
- AI coding instructions (Copilot/LLM)
- ADR template for documenting decisions

### Subtree vs. Submodule

| Feature | Git Subtree | Git Submodule |
|---------|-------------|---------------|
| Clone behavior | Content included automatically | Requires `git submodule update --init` |
| History | Integrated into parent repo | Tracked separately |
| User experience | Transparent to consumers | Visible `.gitmodules` |
| Update complexity | Manual `git subtree pull` | Manual `git submodule update` |
| Best for | Stable shared specs | External dependencies |

---

## Project-Specific READMEs

This README documents the template. When creating a **project-specific repository** (e.g., for a domain like NiceLabel, banking, healthcare), create a project-specific README that:

1. Documents your architecture and systems
2. Describes how you've configured git subtrees from this template
3. Lists which Copilot skills apply to your domain
4. Includes project-specific best practices
5. Documents your ADRs and key architectural decisions

**Example:** See [SCRIB Etiqueteuse](https://github.com/a-scolan/SCRIB_Etiqueteuse) for a project-specific README that extends this template.

---

## Troubleshooting

### Diagrams Not Showing

- Ensure `likec4.config.json` has `"include": { "paths": ["../shared"] }`
- Run `npx likec4 start` from workspace root
- Check for syntax errors in `.c4` files

### IntelliSense Not Working

- Install LikeC4 VS Code extension
- Ensure `"$schema"` is set in `likec4.config.json`
- Reload VS Code window

### Element Not Found

- Use fully qualified names (FQN): `mySystem.api -[calls]-> mySystem.database`
- Check element names match exactly (case-sensitive)
- Ensure elements are defined before referenced

---

## Additional Resources

- **Shared Specifications**: `projects/shared/SPEC_CHEATSHEET.md`
- **Example Projects**:
  - `projects/legacy/` - Simple monolithic architecture
  - `projects/refactored/` - Complex microservices with deployment
  - `projects/spec-showcase/` - All element type examples
- **MCP Servers** (used by Copilot skills):
  - LikeC4 MCP: Query architecture models
  - Context7 MCP: Query LikeC4 documentation (use `/likec4/likec4`)

---

**Ready to document your architecture!** Start with `likec4.config.json`, then update `system-model.c4` with your system's structure.
