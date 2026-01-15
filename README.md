# LikeC4 Project Template

This is a minimal, ready-to-use template for creating new LikeC4 architecture documentation projects. It includes the essential files and follows best practices from the c4_hands-on-demo repository.

## Quick Start

### 1. Copy the Template

```bash
# Copy this template folder to create a new project
cp -r projects/template projects/my-new-project
cd projects/my-new-project
```

### 2. Configure Your Project

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

### 3. Update the Model

Edit `system-model.c4` to define your architecture:

- Replace `mySystem` with your system name
- Update actors (users, external systems)
- Define containers (applications, databases, services)
- Add relationships between elements

### 4. Customize Views

Edit `system-views.c4` to control visualizations:

- Update view titles and descriptions
- Adjust `include` statements to show relevant elements
- Use `rank` to control layout

### 5. Preview Your Diagrams

```bash
# From the workspace root
npx likec4 start

# Then open http://localhost:3000
```

---

## File Structure

This template includes three essential files:

| File | Purpose | Required |
|------|---------|----------|
| `likec4.config.json` | Project configuration (name, includes, aliases) | ✅ Yes |
| `system-model.c4` | Logical architecture (actors, systems, containers, relationships) | ✅ Yes |
| `system-views.c4` | Visualization definitions (C1 context, C2 containers) | ✅ Yes |

### Optional Files (Add When Needed)

You can extend your project by adding:

- **`system-sequences.c4`** - Dynamic views showing use case flows (see `projects/legacy/system-sequences.c4`)
- **`deployment.c4`** - Physical infrastructure (environments, VMs, networks) (see `projects/refactored/deployment.c4`)
- **`deployment-views.c4`** - Infrastructure topology views (see `projects/refactored/deployment-views.c4`)

---

## Best Practices

### Element Naming

✅ **Use PascalCase with Category_Subtype pattern:**

```likec4
Actor_Person           // ✅ Correct
System_Existing        // ✅ Correct
Container_Api          // ✅ Correct

actor_person           // ❌ Wrong (lowercase)
ActorPerson            // ❌ Wrong (no category separator)
```

### Typed Relationships

✅ **All static relationships MUST have explicit kinds:**

```likec4
// Model relationships
api -[calls]-> service 'Invokes'         // ✅ Correct
api -[reads]-> database 'Queries'        // ✅ Correct
worker -[async]-> queue 'Consumes'       // ✅ Correct
api -[writes]-> storage 'Saves to'       // ✅ Correct

api -> service 'Invokes'                 // ❌ Wrong (no kind)
```

### Descriptions and Technology

✅ **Always include descriptions and technology:**

```likec4
api = Container_Api 'API Server' {
  technology 'Node.js, Express'          // ✅ Required for containers
  description 'Handles business logic'   // ✅ Required for all elements
}
```

### Relationship Labels

✅ **Provide descriptive labels for all relationships:**

```likec4
webapp -[calls]-> api 'Makes API requests' {
  description 'HTTPS REST calls'         // Optional: additional details
}

webapp -[calls]-> api                    // ❌ Wrong (no label)
```

### View Patterns

✅ **Use scoped wildcards for focused views:**

```likec4
view c2_containers {
  include mySystem.*                     // ✅ All containers in mySystem
  include mySystem.* -> *                // ✅ Outgoing relationships
  include * -> mySystem.*                // ✅ Incoming relationships
  
  include ** -> **                       // ❌ Avoid (too broad)
}
```

✅ **Use rank for layout control:**

```likec4
view c1_context {
  include user, mySystem, emailService
  
  rank source { user }                   // Actors at the top
  rank sink { emailService }             // External systems at bottom
}
```

### No Return Relationships

❌ **Responses are implicit - don't create return relationships:**

```likec4
client -[calls]-> server 'Requests data'    // ✅ Correct

// ❌ Wrong: don't add the return
client -[calls]-> server 'Requests data'
server -[calls]-> client 'Returns response'
```

---

## Element Kinds Reference

Available element kinds from `projects/shared/`:

### Actors (C1)
- `Actor_Person` - Individual user
- `Actor_Staff` - Internal staff member
- `Actor_Admin` - System administrator

### Systems (C1)
- `System_Existing` - Current system
- `System_New` - Planned system
- `System_Legacy` - Deprecated system
- `System_External` - Third-party system

### Containers (C2)
- `Container_Api` - API service
- `Container_WebApp` - Web application
- `Container_Database` - Database
- `Container_Queue` - Message queue
- `Container_Cache` - Cache service
- `Container_WebServer` - Web server (nginx, Apache)
- `Container_LoadBalancer` - Load balancer
- `Container_Storage` - Object/file storage
- And 20+ more in `projects/shared/spec-containers.c4`

### Components (C3)
- `Component` - Internal module/class

### Relationship Kinds

**Model relationships** (business logic):
- `calls` - Synchronous invocation
- `async` - Asynchronous communication
- `reads` - Data retrieval
- `writes` - Data persistence
- `uses` - General usage

**Deployment relationships** (infrastructure):
- `http`, `https`, `tcp` - Network protocols
- `nfs`, `amqp`, `sql`, `redis` - Specific protocols
- And more in `projects/shared/spec-deployment.c4`

---

## Extending the Template

### Adding Component (C3) Views

1. Add components inside containers in `system-model.c4`:

```likec4
api = Container_Api 'API Server' {
  technology 'Node.js'
  
  router = Component 'Router' {
    technology 'Express Router'
    description 'Routes HTTP requests'
  }
  
  authMiddleware = Component 'Auth Middleware' {
    technology 'Passport.js'
    description 'Validates JWT tokens'
  }
}
```

2. Add C3 view in `system-views.c4`:

```likec4
view c3_api_components {
  title 'C3 / API Components'
  
  include user
  include mySystem.api.*              // All components in API
  include mySystem.database
}
```

### Adding Dynamic Sequences

Create `system-sequences.c4` (copy structure from `projects/legacy/system-sequences.c4`):

```likec4
dynamic view sequence_user_login {
  title 'Use Cases / User Login'
  
  user -> mySystem.webapp 'Opens login page'
  mySystem.webapp -> mySystem.api 'POST /api/auth/login'
  mySystem.api -> mySystem.database 'Verify credentials'
  mySystem.api -> mySystem.webapp 'Return JWT token'
}
```

### Adding Deployment Views

Create `deployment.c4` and `deployment-views.c4` (see `projects/refactored/deployment*.c4` for full examples).

---

## Common Workflows

### 1. Document a New System

1. Define the system boundary in `system-model.c4`
2. Add actors who interact with it
3. Define containers (apps, databases, services)
4. Add relationships with typed kinds
5. Create C1 and C2 views in `system-views.c4`

### 2. Add an External Dependency

```likec4
// In system-model.c4
externalService = System_External 'Payment Gateway' {
  technology 'Stripe API'
  description 'Handles payment processing'
  #External
}

mySystem.api -[calls]-> externalService 'Process payments'
```

### 3. Model Async Communication

```likec4
// In system-model.c4
queue = Container_Queue 'Message Queue' {
  technology 'RabbitMQ'
  description 'Async job processing'
}

api -[async]-> queue 'Publishes jobs'
worker -[async]-> queue 'Consumes jobs'
```

### 4. Filter Views with Tags

```likec4
// Tag elements
api = Container_Api 'API' {
  #Service #Production
}

// Filter in views
view production_services {
  include * where tag is #Production
}
```

---

## Additional Resources

- **Shared Specifications**: See `projects/shared/SPEC_CHEATSHEET.md` for complete reference
- **Example Projects**:
  - `projects/legacy/` - Simple monolithic architecture
  - `projects/refactored/` - Complex microservices with full deployment
  - `projects/spec-showcase/` - Catalog of all element types
- **Main README**: See workspace root `README.md` for installation and best practices

---

## Troubleshooting

### Diagrams Not Showing

- Ensure `likec4.config.json` has correct `"include": { "paths": ["../shared"] }`
- Run `npx likec4 start` from workspace root, not project folder
- Check console for syntax errors in `.c4` files

### IntelliSense Not Working

- Install LikeC4 VS Code extension
- Ensure `"$schema"` is set in `likec4.config.json`
- Reload VS Code window

### Element Not Found Errors

- Use fully qualified names (FQN) in relationships: `mySystem.api -[calls]-> mySystem.database`
- Check element names match exactly (case-sensitive)
- Ensure elements are defined before being referenced

---

**Ready to document your architecture!** Start by customizing `likec4.config.json`, then update `system-model.c4` with your system's structure.
