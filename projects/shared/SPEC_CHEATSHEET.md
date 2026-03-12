# LikeC4 Specification Cheat Sheet

**Quick reference guide for element kinds, tags, colors, and hierarchies used in this workspace.**

📁 **Spec Location:** [`projects/shared/`](../projects/shared/)

---

## 🏗️ Element Hierarchy (C4 Levels)

### C1 - Context Level: Actors & Systems
**File:** [`spec-context.c4`](../projects/shared/spec-context.c4)

```
Actor (base)
├── Actor_Person      #Actor #Person      → External users (blue)
├── Actor_Staff       #Actor #Staff       → Internal users (green)
└── Actor_Admin       #Actor #Admin       → Administrators (amber)

System (variants)
├── System_New        #System #New        → New systems (green)
├── System_Existing   #System #Existing   → Current systems (blue)
├── System_Legacy     #System #Legacy     → Deprecated (slate gray)
└── System_External   #System #External   → 3rd party (red)
```

**Usage:**
```likec4
customer = Actor_Person 'Customer'
vault = System_Existing 'Vault System'
oldBackup = System_Legacy 'Legacy Backup'
virusTotal = System_External 'VirusTotal API'
```

---

### C2 - Container Level: Applications & Services
**File:** [`spec-containers.c4`](../projects/shared/spec-containers.c4)

```
Container (base)                           #Container → Generic application container
│
├── 🌐 Network & Security
│   ├── Container_ReverseProxy             #Container #ReverseProxy → Reverse proxy
│   ├── Container_Waf                      #Container #Waf → Web Application Firewall
│   ├── Container_Loadbalancer             #Container #Loadbalancer → Load balancer
│   └── Container_Firewall                 #Container #Firewall → Firewall
│
├── 💻 Client Applications
│   ├── Container_Browser                  #Container #Browser → Web browser
│   ├── Container_MobileApp                #Container #MobileApp → Mobile app
│   └── Container_Spa                      #Container #Spa → Single page application
│
├── 🚀 Application Servers
│   ├── Container_Webapp                   #Container #Webapp → Web application
│   ├── Container_Api                      #Container #Api → API / Service
│   │   └── Container_Api_Geo              #Container #Api #Geo → Mapping API
│   ├── Container_WebServer                #Container #WebServer → Web server
│   ├── Container_ApplicationServer        #Container #ApplicationServer → Application server
│   ├── Container_ProcessingServer         #Container #ProcessingServer → Processing server
│   ├── Container_ExchangeServer           #Container #ExchangeServer → Exchange server
│   ├── Container_IamServer                #Container #IamServer → IAM server
│   └── Container_Mailserver               #Container #Mailserver → Mail server
│
├── 💬 Messaging
│   └── Container_Queue                    #Container #Queue → Message queue
│
└── 💾 Data & Storage
    ├── Container_Database                 #Container #Database → Database (storage shape/color)
    │   └── Container_Database_Geo         #Container #Database #Geo → Geo data warehouse
    ├── Container_Directory                #Container #Directory → Directory (LDAP)
    ├── Container_DataServer               #Container #DataServer → Data server (storage)
    ├── Container_FileServer               #Container #FileServer → File server (storage)
    └── Storage                            #Container → Object storage (storage shape/color)
```

**Usage:**
```likec4
api = Container_Api 'Upload API' { technology 'Node.js' }
queue = Container_Queue 'Job Queue' { technology 'RabbitMQ' }
db = Container_Database 'Metadata DB' { technology 'MongoDB' }
storage = Storage 'Object Store' { technology 'MinIO' }
webServer = Container_WebServer 'Web Server' { technology 'Apache' }
fileServer = Container_FileServer 'File Server' { technology 'NFS' }
```

---

### C3 - Component Level
**File:** [`spec-components.c4`](../projects/shared/spec-components.c4)

```
Component                       #Component → Internal building blocks
```

**Usage:**
```likec4
controller = Component 'Upload Controller'
validator = Component 'File Validator'
encryptor = Component 'Encryption Service'
```

---

## 🏷️ Tag Taxonomy

### Global Tags (Purpose & Platform)
**File:** [`spec-global.c4`](../projects/shared/spec-global.c4)

| Tag | Color | Meaning |
|-----|-------|---------|
| `#Internal` | Blue `rgb(59, 130, 246)` | Internal systems |
| `#External` | Red `rgb(220, 38, 38)` | External/3rd party |
| `#Legacy` | Slate `rgb(148, 163, 184)` | Deprecated systems |
| `#Cloud` | Sky Blue `rgb(14, 165, 233)` | Cloud-hosted |
| `#Saas` | Green `rgb(34, 197, 94)` | SaaS platforms |
| `#Queue` | Amber `rgb(251, 191, 36)` | Message queues |
| `#Security` | Red `rgb(220, 38, 38)` | Security concerns |

---

### Deployment Tags (Infrastructure)
**File:** [`spec-deployment.c4`](../projects/shared/spec-deployment.c4)

#### Family Tags
| Tag | Purpose |
|-----|---------|
| `#Zone` | Network zones |
| `#Node` | Infrastructure nodes |
| `#Infra` | Infrastructure services |

#### Network Zone Tags
| Tag | Description |
|-----|-------------|
| `#Internet` | Public internet |
| `#Vlan` | Virtual LANs |
| `#Lan` | Physical LANs |
| `#Subnet` | IP subnets |

#### Infrastructure Node Tags
| Tag | Description |
|-----|-------------|
| `#Cluster` | Server clusters |
| `#Vm` | Virtual machines |
| `#Server` | Physical servers |
| `#App` | Application instances |
| `#AppBrowser` | Browser clients |
| `#AppMobile` | Mobile apps |
| `#AppRich` | Rich clients |

#### Infrastructure Service Tags
| Tag | Description |
|-----|-------------|
| `#F5` | F5 load balancers |
| `#Fw` | Firewalls |
| `#Router` | Network routers |

#### Environment Tags (Colored)
| Tag | Color | Purpose |
|-----|-------|---------|
| `#Production` | Green `rgb(5, 150, 105)` | Production environment |
| `#Development` | Orange `rgb(251, 146, 60)` | Dev environment |
| `#Environment` | - | Generic environment |
| `#Datacenter` | - | Data center |
| `#Cicd` | - | CI/CD infrastructure |

#### Infrastructure Category Tags (Colored)
| Tag | Color | Purpose |
|-----|-------|---------|
| `#Infrastructure` | Blue `rgb(2, 132, 199)` | Core infrastructure |
| `#Networking` | Blue `rgb(37, 99, 235)` | Network layer |
| `#SharedInfra` | Purple `rgb(139, 92, 246)` | Shared services |

#### Deployment Pattern Tags (Colored)
| Tag | Color | Purpose |
|-----|-------|---------|
| `#Deployment` | Purple `rgb(84, 34, 170)` | Deployment targets |
| `#Ingress` | Green `rgb(34, 197, 94)` | Entry points |
| `#Routing` | Blue `rgb(59, 130, 246)` | Traffic routing |

#### Deployment Tier Tags (Colored) 🆕
| Tag | Color | Purpose | Usage |
|-----|-------|---------|-------|
| `#Dmz` | Red `rgb(220, 38, 38)` | DMZ security zone | Edge services, reverse proxy, SSL termination |
| `#AppTier` | Blue `rgb(59, 130, 246)` | Application tier | Business logic, Web UI, API servers |
| `#ProcTier` | Purple `rgb(168, 85, 247)` | Processing tier | CPU-intensive workloads, transcoding, ML |
| `#DataTier` | Gray `rgb(75, 85, 99)` | Data persistence tier | Databases, cache, object storage |

**Tag-Based Filtering Example:**
```likec4
deployment view dmz_tier {
  title 'DMZ Tier - Edge Services'
  include element.tag == #Dmz  // Includes all DMZ zone elements automatically
  autoLayout TopBottom
}
```

#### Messaging/Async Tags (Colored)
| Tag | Color | Purpose |
|-----|-------|---------|
| `#Messaging` | Amber `rgb(251, 191, 36)` | Message systems |
| `#Async` | Orange `rgb(251, 146, 60)` | Async processing |

#### Data/Storage Tags (Colored)
| Tag | Color | Purpose |
|-----|-------|---------|
| `#Persistence` | Gray `rgb(107, 114, 128)` | Data persistence |
| `#Data` | Dark Gray `rgb(75, 85, 99)` | Data stores |
| `#Backup` | Indigo `rgb(99, 102, 241)` | Backup systems |
| `#Recovery` | Light Indigo `rgb(129, 140, 248)` | Disaster recovery |

#### Service/Application Tags (Colored)
| Tag | Color | Purpose |
|-----|-------|---------|
| `#Service` | Blue `rgb(59, 130, 246)` | Application services |
| `#Monitoring` | Purple `rgb(168, 85, 247)` | Monitoring tools |
| `#Observability` | Light Purple `rgb(192, 132, 250)` | Observability stack |

#### CI/CD Tags (Colored)
| Tag | Color | Purpose |
|-----|-------|---------|
| `#Pipeline` | Pink `rgb(236, 72, 153)` | CI/CD pipelines |
| `#DeploymentAutomation` | Purple `rgb(168, 85, 247)` | Automation tools |

---

## 🎨 Custom Colors

**File:** [`spec-global.c4`](../projects/shared/spec-global.c4)

| Color Name | Hex | Usage |
|------------|-----|-------|
| `legacy` | `#94a3b8` | Deprecated systems (slate gray) |
| `modern` | `#3b82f6` | New/current containers (blue) |
| `external` | `#ef4444` | External systems (red) |
| `storage` | `#f59e0b` | Storage/databases (orange) |

**Example:**
```likec4
element System_Legacy {
  style { color legacy }  // Uses #94a3b8
}
```

---

## 🔗 Relationship Types

### Model Relationships (Business Logic)
**File:** [`spec-global.c4`](../projects/shared/spec-global.c4)

| Type | Notation | Style | Usage |
|------|----------|-------|-------|
| `uses` | 'Uses' | Solid | Generic usage |
| `calls` | 'Calls' | Solid, Blue | Synchronous calls |
| `async` | 'Async' | Dashed, Blue | Asynchronous messaging |
| `reads` | 'Reads' | Solid, Green | Data reads |
| `writes` | 'Writes' | Solid, Amber | Data writes |

**Example:**
```likec4
customer -[calls]-> portal 'Uses UI' {
  technology 'Manual'
}

api -[reads]-> database 'Fetches metadata' {
  technology 'PostgreSQL'
}

api -[async]-> queue 'Publishes job' {
  technology 'AMQP'
}
```

**Common relationship technology values:** `Manual`, `HTTPS`, `HTTP/8080`, `AMQP`, `PostgreSQL`, `SQL`, `LDAP`, `SMTP`, `OIDC/SAML`, `NFS`

**Rule:** Put interaction technology on the **system-model relationship**. Add a port only when it is non-default for the protocol.

---

### Deployment Relationships (Infrastructure)
**File:** [`spec-deployment.c4`](../projects/shared/spec-deployment.c4)

Use these deployment relationships only for **infrastructure-specific** connections. Normal application traffic should usually be modeled in the system model and inherited in deployment through `instanceOf`.

#### Network Protocols
| Type | Notation |
|------|----------|
| `http` | 'HTTP' |
| `https` | 'HTTPS' |
| `tcp` | 'TCP' |
| `nfs` | 'NFS' |
| `amqp` | 'AMQP' |

#### Service Links
| Type | Notation | Color | Usage |
|------|----------|-------|-------|
| `oidc_saml` | 'Authentication' | Red | Auth flows |
| `ldap` | 'LDAP' | Blue | Directory access |
| `sql` | 'SQL' | Amber | Database queries |
| `redis` | 'REDIS' | Green | Cache access |
| `smtp` | 'SMTP' | Indigo | Email delivery |

**Example:**
```likec4
frontendVm -[https]-> apiVm 'Ingress traffic'
backupVm -[nfs]-> archiveVm 'Replicates backups'
```

---

## 🏢 Deployment Node Kinds

**File:** [`spec-deployment.c4`](../projects/shared/spec-deployment.c4)

### Styled Deployment Nodes (PascalCase)

```
Node_Environment               #Node #Environment → Environment containers
  ├── Zone                     #Zone              → Network zones (generic)
  │   ├── Zone_Internet        #Zone #Internet    → Public internet zone
  │   ├── Zone_Vlan            #Zone #Vlan        → VLAN segments
  │   ├── Zone_Lan             #Zone #Lan         → Physical LANs
  │   └── Zone_Subnet          #Zone #Subnet      → IP subnets
  │
  ├── Node_Cluster             #Node #Cluster     → Server clusters
  ├── Node_Vm                  #Node #Vm          → Virtual machines
  ├── Node_Server              #Node #Server      → Physical servers
  ├── Node_App                 #Node #App         → App instances
  │   ├── Node_AppBrowser      #Node #AppBrowser  → Browser clients
  │   ├── Node_AppMobile       #Node #AppMobile   → Mobile clients
  │   └── Node_AppRich         #Node #AppRich     → Rich clients
  │
  ├── Infra_F5                 #Infra #F5         → F5 load balancers
  ├── Infra_Fw                 #Infra #Fw         → Firewalls
  ├── Infra_Router             #Infra #Router     → Routers
  │
  ├── Node_Datacenter          #Node #Datacenter  → Data centers
  └── Node_Cicd                #Node #Cicd        → CI/CD infra
```

**Usage:**
```likec4
deployment {
  Node_Environment Prod 'Production' {
    Zone Dmz 'DMZ' {
      Node_Vm apiVm 'API Server' {
        Node_App apiApp {
          instanceOf vault.api
        }
      }
    }
  }
}
```

---

## 📝 Naming Conventions

### PascalCase for All Public Names
**✅ Correct:**
```likec4
#Production #Infrastructure #Deployment
Actor_Person, System_Legacy, Container_Api
Node_Environment, Zone_Vlan, Node_Vm
```

**❌ Incorrect:**
```likec4
#production #infrastructure #deployment
actor_person, system_legacy, container_api
node_environment, zone_vlan, node_vm
```

### Element Naming Pattern
**Format:** `Category_Subtype`

- `Actor_Person`, `Actor_Staff`, `Actor_Admin`
- `System_New`, `System_Existing`, `System_Legacy`, `System_External`
- `Container_Api`, `Container_Database`, `Container_Queue`
- `Node_Environment`, `Node_Vm`, `Node_App`
- `Zone_Internet`, `Zone_Vlan`, `Zone_Lan`

---

## 🎯 Quick Reference: When to Use What

### Context Diagrams (C1)
```likec4
customer = Actor_Person 'Customer'
vault = System_Existing 'Vault System'
virusTotal = System_External 'VirusTotal API'

customer -> vault { uses 'Uploads files' }
vault -> virusTotal { calls 'Scans files' }
```

### Container Diagrams (C2)
```likec4
api = Container_Api 'Upload API'
queue = Container_Queue 'Job Queue'
worker = Container_Webapp 'Worker'
db = Container_Database 'MongoDB'
storage = Storage 'MinIO'

api -> queue { async 'Publishes job' }
worker -> storage { writes 'Stores file' }
worker -> db { writes 'Saves metadata' }
```

### Component Diagrams (C3)
```likec4
controller = Component 'Upload Controller'
validator = Component 'File Validator'
publisher = Component 'Queue Publisher'

controller -> validator { calls 'Validates file' }
controller -> publisher { calls 'Publishes job' }
```

### Deployment Diagrams
```likec4
deployment {
  Node_Environment Prod 'Production' {
    #Production
    
    Zone AppTier 'Application Tier' {
      #Infrastructure
      
      Node_Vm apiVm 'API Server' {
        Node_App apiApp {
          instanceOf vault.api
        }
      }
    }
  }
}
```

---

## 🔍 Filtering by Tags

### View Filters
```likec4
view {
  include
    * where tag is #Production,
    * where tag is #Infrastructure,
    * where tag is #Vm
}
```

### Common Patterns
```likec4
// Show only VMs in production
* where tag is #Production and tag is #Vm

// Show all external systems
* where tag is #External

// Show all async messaging
* where tag is #Async or tag is #Queue

// Show all data persistence
* where tag is #Database or tag is #Storage
```

---

## 📚 See Also

- **[README.md](../README.md)** - Project overview and setup
- **[Best Practices](../README.md#-best-practices--standards)** - Modeling standards
- **[Architecture Decisions](../ARCHITECTURE_DECISIONS.md)** - Why certain technologies were chosen
- **[LikeC4 DSL Documentation](https://likec4.dev/dsl/)** - Official language reference

---

**Last Updated:** January 2026  
**Maintained by:** Architecture Team
