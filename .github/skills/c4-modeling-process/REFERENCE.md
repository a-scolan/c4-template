# C4 Modeling Reference

Detailed explanations, examples, and clarifications for C4 modeling process.

## C4 Framework Levels

### C1 - System Context

**Purpose:** Show system boundary, who uses it, what it integrates with.

**Audience:** Everyone (business stakeholders, developers, operations)

**Content:**
- The system being documented
- Users and roles (people and systems)
- External systems and services
- High-level relationships

**Example:**

```likec4
model {
  // Your system
  corePlatform = System_Existing 'Core Platform' {
    description 'Shared digital platform with secure document workflows'
  }
  
  // Users
  customer = Actor_Person 'Customer' {
    description 'End user'
  }
  
  // External systems
  scanner = System_External 'Virus Scanner' {
    description 'Cloud antivirus service'
  }
  
  // Relationships
  customer -[calls]-> corePlatform 'Uploads and retrieves files'
  corePlatform -[calls]-> scanner 'Scans uploaded files'
}
```

### C2 - Container

**Purpose:** Show major building blocks of the system and their interactions.

**Audience:** Architects, developers, operations

**Content:**
- Containers (applications, services, databases, message queues)
- Technologies for each container
- Communication patterns (sync API calls, async messages, data flows)

**What is a Container?**

A container is a **runtime boundary** - something that must be running for the system to work:

**Examples of containers:**
- Web application (Node.js, Django, Spring Boot)
- Single-page application (React in browser)
- Mobile application
- Microservice
- Database instance
- Message queue
- Object storage
- Serverless function

**NOT containers:**
- Classes or modules (those are code organization)
- Folders or packages (code structure)
- Layers (architectural concept, not deployment unit)

**Key test:** Can it be deployed independently? Does it have its own process space?

**Example:**

```likec4
model {
  corePlatform = System_Existing 'Core Platform' {
    // Frontend container
    webApp = Container_Spa 'Web App' {
      technology 'React'
      description 'User interface for file management'
    }
    
    // Backend containers
    api = Container_Api 'API Gateway' {
      technology 'Kong'
      description 'Routes and validates requests'
    }
    
    uploadService = Container_Api 'Upload Service' {
      technology 'Node.js'
      description 'Handles file uploads and validation'
    }
    
    // Data containers
    database = Container_Database 'Document DB' {
      technology 'MongoDB'
      description 'File metadata storage'
    }
    
    storage = Container_ObjectStorage 'Object Storage' {
      technology 'MinIO'
      description 'Encrypted file storage'
    }
    
    // Processing containers
    queue = Container_Queue 'Job Queue' {
      technology 'RabbitMQ'
      description 'Async processing queue'
    }
    
    worker = Container_ProcessingServer 'Worker' {
      technology 'Go'
      description 'Background file processing'
    }
  }
  
  // Relationships
  webApp -[calls]-> api 'HTTPS/443'
  api -[calls]-> uploadService 'Routes upload requests'
  uploadService -[async]-> queue 'Queue processing job'
  queue -[async]-> worker 'Deliver job'
  worker -[writes]-> database 'Update metadata'
  worker -[writes]-> storage 'Save encrypted file'
}
```

### C3 - Component

**Purpose:** Show internal structure of a container by grouping related code.

**Audience:** Developers

**Content:**
- Components (logical groupings of related classes/code)
- Interfaces between components
- Internal communication patterns

**What is a Component?**

A component is a **grouping of related functionality** behind a well-defined interface:

- **NOT separately deployable** (only containers are)
- **Executes in container's process space**
- **Groups related classes/functions**
- **May span multiple files/modules**

**Examples of components:**
- Authentication module (login, JWT validation, session management)
- Business logic layer (domain rules, validation, orchestration)
- Data access layer (repository pattern, database queries)
- API router (endpoint definitions, middleware)

**NOT components:**
- Individual classes (too granular)
- Individual files (code organization)
- Folders or packages (structural, not functional)

**Key test:** Does it group related functionality with a clear responsibility?

**Example:**

```likec4
model {
  mySystem = System_Existing 'My System' {
    uploadService = Container_Api 'Upload Service' {
    // Components
      validateModule = Component 'Validation' {
        description 'File validation (size, type, malware check)'
      }
      
      queueModule = Component 'Queue Publisher' {
        description 'Publishes validated jobs to queue'
      }
      
      // Internal relationships
      validateModule -[uses]-> queueModule 'Publish if valid'
    }
  }
}
```

### C4 - Code

**Purpose:** Show classes, interfaces, methods (typically as actual code, not diagrams).

**Audience:** Developers

**Content:**
- Class diagrams (UML)
- ER diagrams (database schemas)
- Source code itself

**C4 diagrams typically don't include this level** - the code IS the documentation.

## Container vs Component Distinction

### Container

**Definition:** Runtime boundary, independently deployable

**Characteristics:**
- Has own process space
- Can be deployed separately
- Has independent scaling
- May run on different servers
- Technology stack can differ

**Examples:**
```
Web UI (React SPA in browser)
API (Node.js on server)
Database (PostgreSQL instance)
Worker (Go service)
Queue (RabbitMQ)
```

### Component

**Definition:** Code-level grouping, not separately deployable

**Characteristics:**
- Executes within container's process
- Cannot deploy alone
- Shares container's technology
- Logical grouping of related code
- Has well-defined interface

**Examples:**
```
Authentication module
Business logic layer
Data repository
API router
```

### Practical Example

```likec4
// CONTAINER LEVEL (C2)
model {
  mySystem = System_Existing 'My System' {
    uploadService = Container_Api 'Upload Service' {
    technology 'Node.js'
    description 'Handles file uploads'
    }
  
    database = Container_Database 'Database' {
      technology 'MongoDB'
      description 'Stores metadata'
    }
  
    // These are separate deployable units
    uploadService -[writes]-> database 'Persist metadata'
  }
}

// COMPONENT LEVEL (C3)
model {
  mySystem = System_Existing 'My System' {
    uploadService = Container_Api 'Upload Service' {
      // These execute within uploadService's Node.js process
      validator = Component 'Validator' {
        description 'Validates uploads'
      }
      
      repository = Component 'Data Access' {
        description 'Database queries'
      }
      
      // Internal communication (same process space)
      validator -[uses]-> repository 'Save validated data'
    }
  }
}
```

## Deployment Diagrams

**Purpose:** Show how software maps to infrastructure.

**When to create:**
- Multiple environments (dev, staging, production)
- Infrastructure matters (VMs, zones, networking)
- Deployment strategy is complex

**Content:**
- Environments (production, staging, dev)
- Infrastructure nodes (VMs, servers, zones)
- Deployed instances of containers
- Network relationships

**Example:**

```likec4
deployment {
  Prod = Node_Environment 'Production' {
    #Production
    
    AppTier = Zone 'App Tier (VLAN 101: 10.1.0.0/24)' {
      description """
        Application services zone
        
        | Property | Value |
        |:---------|:------|
        | VLAN | 101 |
        | Network | 10.1.0.0/24 |
      """
      
      ProdApiVm = Node_Vm 'prod-api-vm' {
        technology 'Node.js + Docker'
        description """
          | Property | Value |
          |:---------|:------|
          | IP | 10.1.0.10/24 |
          | Port | 3000 |
        """
        
        apiApp = Node_App 'API' {
          instanceOf corePlatform.api
        }
      }
    }
  }
}
```

## Dynamic Diagrams

**Purpose:** Show runtime behavior for specific use cases.

**When to create:**
- Complex workflows need explanation
- Integration patterns are non-obvious
- Multiple systems coordinate
- Async processing flows

**Content:**
- Temporal sequence of interactions
- Step-by-step flow through system
- Actor-initiated workflows

**Example:**

```likec4
views 'Use Cases' {
  dynamic view upload_flow {
    title 'Document Upload'
    
    customer -> corePlatform.webApp 'Upload file'
    corePlatform.webApp -> corePlatform.api 'POST /upload'
    corePlatform.api -> corePlatform.uploadService 'Route to upload service'
    corePlatform.uploadService -> corePlatform.queue 'Queue processing job'
    corePlatform.queue -> corePlatform.worker 'Deliver job'
    corePlatform.worker -> corePlatform.storage 'Store encrypted file'
    corePlatform.worker -> corePlatform.database 'Update metadata'
  }
}
```

**Guidelines:**
- Create 2-5 dynamic diagrams maximum (not every interaction)
- Show interesting/complex patterns
- Always start with initiating actor
- Place in `views 'Use Cases'` folder, never C1

## View Organization Rules

### Mandatory Structure

```likec4
// Index view (ONLY at root)
views {
  view index extends c1_context { }
}

// All other views in category folders
views 'C1' {
  view c1_context { }
}

views 'C2' {
  view c2_containers { }
  view c2_focused_workflow { }  // Optional focused views
}

views 'C3' {
  view c3_container_name { }  // One per complex container
}

views 'Use Cases' {
  dynamic view workflow_name { }
}

views 'Deployment' {
  deployment view environment_name { }
}
```

### Context Requirements

**Every view must show parent/surrounding context:**

| View Type | Must Include |
|-----------|--------------|
| C3 Component | Parent container boundary |
| C2 Container | Parent system boundary |
| Deployment VM | Parent zone |
| Dynamic | Initiating actor |

**Example - C3 with context:**

```likec4
views 'C3' {
  view c3_upload_service {
    title 'Upload Service Internals'
    
    // Parent context
    include corePlatform        // System boundary
    include corePlatform.*      // Neighboring containers
    
    // Focus area
    include corePlatform.uploadService     // Container boundary
    include corePlatform.uploadService.*   // Internal components
    
    // Related elements
    include -> corePlatform.uploadService.* // What calls in
    include corePlatform.uploadService.* -> // What calls out
  }
}
```

## Common Anti-Patterns

### Anti-Pattern: Bottom-Up Design

❌ **Problem:** Starting with classes/code and working up

```
Developer: "We have UserService, OrderService, PaymentService classes... 
            let's make those into containers."
```

✅ **Solution:** Start with system boundary (C1), then break into independent deployment units (C2)

```
1. C1: What is the system? Who uses it?
2. C2: What independently deployable pieces make the system work?
3. C3: What are the internal groupings within complex containers?
```

### Anti-Pattern: Too Many Containers

❌ **Problem:** Every class becomes a container

```likec4
// DON'T: These are classes, not containers
userController = Container 'UserController' { }
userService = Container 'UserService' { }
userRepository = Container 'UserRepository' { }
```

✅ **Solution:** Containers are runtime boundaries

```likec4
// DO: Group related classes into deployable unit
api = Container_API 'User API' {
  description 'User management service containing controllers, services, repositories'
  technology 'Spring Boot'
}
```

### Anti-Pattern: Too Many Components

❌ **Problem:** Creating C3 views for every container

```
System has 20 containers → Creates 20 C3 component views
```

✅ **Solution:** C3 only for complex/critical containers

```
System has 20 containers → Create 2-3 C3 views for most complex ones
```

### Anti-Pattern: Inconsistent Naming

❌ **Problem:** Mixed naming conventions

```
api_gateway, ApiGateway, api-gateway, apiGateway (all different elements)
```

✅ **Solution:** Consistent naming

```
Element kinds: PascalCase (Container_Api, Node_Vm)
Variables: camelCase (apiGateway, prodVm)
View IDs: snake_case (c1_context, c2_containers)
```

### Anti-Pattern: Missing Relationships

❌ **Problem:** Showing structure without communication

```likec4
// Only shows containers, not how they interact
frontend = Container_Spa 'Frontend' { }
api = Container_API 'API' { }
database = Container_Database 'DB' { }
```

✅ **Solution:** Document all significant relationships

```likec4
frontend = Container_Spa 'Frontend' { }
api = Container_API 'API' { }
database = Container_Database 'DB' { }

frontend -[calls]-> api 'Makes requests'
api -[reads]-> database 'Queries data'
api -[writes]-> database 'Updates records'
```

### Anti-Pattern: Unclear Container Names

❌ **Problem:** Generic names that don't describe purpose

```
service1 = Container_Service 'Service' { }
module2 = Container_Module 'Module' { }
component3 = Container_Component 'Component' { }
```

✅ **Solution:** Descriptive names reflecting domain

```
uploadService = Container_Api 'Upload Service' {
  description 'Handles file upload and validation'
}

authService = Container_Api 'Auth Service' {
  description 'User authentication and authorization'
}
```

### Anti-Pattern: Flow Views in C1

❌ **Problem:** Creating temporal flows at C1 level

```likec4
views 'C1' {
  dynamic view deploymentFlow { }  // WRONG: Flows don't belong in C1
  dynamic view userAccessFlow { }  // WRONG: C1 is static only
}
```

✅ **Solution:** Flows belong in 'Use Cases', require C2+ elements

```likec4
views 'C1' {
  view c1_context { }  // Static system boundary only
}

views 'Use Cases' {
  dynamic view deploymentFlow { }  // Correct: Shows container interactions
  dynamic view userAccessFlow { }  // Correct: Shows runtime behavior
}
```

## Further Reading

- **C4 Model Home:** https://c4model.com/
- **System Context:** https://c4model.com/diagrams/system-context
- **Container:** https://c4model.com/diagrams/container
- **Component:** https://c4model.com/diagrams/component
- **Deployment:** https://c4model.com/diagrams/deployment
- **Dynamic:** https://c4model.com/diagrams/dynamic
- **LikeC4 Docs:** https://likec4.dev/
