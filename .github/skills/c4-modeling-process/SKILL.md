---
name: c4-modeling-process
description: Use when planning, reviewing, or correcting a LikeC4 model and you need to decide the right top-down design order (C1→C2→C3), whether C3 detail is warranted, or when to hand off from structural modeling to deployment or dynamic-view skills.
---

# C4 Modeling Process

## Overview

This skill is the **sequencing guide** for LikeC4 work. It decides what level to model next, what can stay out for now, and which specialized skill should take over for the detailed edit.

**Core principle:** design top-down — **C1 Context → C2 Containers → C3 Components**. Add **Dynamic** and **Deployment** only after the structural model is stable enough to support them.

## When to Use

- Starting a new LikeC4 model from a blank page
- Reviewing an existing model that feels too detailed too early
- Deciding whether a container deserves a C3 view
- Deciding whether a requested diagram belongs in C1/C2/C3, `Use Cases`, or `Deployment`
- Coordinating several LikeC4 skills without losing the big picture

**Do not use** for the detailed edit itself when a more specific skill applies:
- use `create-element` for element declarations
- use `create-relationship` for typed relationships
- use `design-view` for static views
- use `create-sequence-view` for dynamic flows
- use `model-deployment-infrastructure` for deployment topology

## Quick Reference

| Stage | Question | Output | Supporting skills |
|---|---|---|---|
| **0. Context** | What project/rules am I editing? | Valid workspace understanding | `understand-project-structure` |
| **1. C1** | What is the system boundary? | Actors, systems, external dependencies | `create-element`, `create-relationship`, `design-view` |
| **2. C2** | What runtime building blocks make it work? | Containers and their interactions | `create-element`, `create-relationship`, `design-view` |
| **3. C3** | Which containers truly need internal detail? | Selected component views only | `create-element`, `create-relationship`, `design-view` |
| **4. Dynamic** | Which workflows need temporal order? | `views 'Use Cases'` dynamic views | `create-sequence-view` |
| **5. Deployment** | Where does it run? | Environments, zones, VMs, instances | `model-deployment-infrastructure` |
| **6. Validate** | Is the model coherent and renderable? | Confidence before commit | `test-model` |

## Supporting Files

- Read `REFERENCE.md` when you need deeper examples, anti-pattern explanations, or a sharper container-vs-component distinction.
- Read `CHECKLIST.md` before signoff when you want a more exhaustive validation pass than the short done-criteria in this file.

## Order of Work

1. **If the workspace is unfamiliar, start with `understand-project-structure`.**
   - confirm project structure, shared specs, valid kinds, and existing view organization
   - do this before inventing new kinds or drilling into details

2. **Model C1 first.**
   - define the system boundary
   - identify actors and external systems
   - keep the view static

3. **Then model C2.**
   - split the system into runtime/deployable containers
   - add relationships that explain how the system actually works

4. **Only create C3 where it earns its keep.**
   - choose containers that are complex, risky, or central to the architecture
   - skip C3 for trivial containers

5. **Add Dynamic views when order-in-time matters.**
   - user workflows, async flows, validation/error paths

6. **Add Deployment views when runtime topology matters.**
   - environments, zones, VMs, deployed apps, `instanceOf`

7. **Validate before finishing.**

## Step 1 — C1 Context

Start by modeling the system in its environment.

```likec4
model {
  user = Actor_Person 'User' {
    description 'End user of the system'
  }

  mySystem = System_Existing 'My System' {
    description 'The main system being documented'
  }

  emailService = System_External 'Email Service' {
    technology 'SendGrid'
    description 'Third-party email delivery service'
  }

  user -[calls]-> mySystem 'Uses'
  mySystem -[calls]-> emailService 'Sends notifications'
}
```

**C1 rule:** this level shows **boundary and environment**, not temporal flow.

```likec4
views 'C1' {
  view c1_context {
    title 'System Context'
    include user
    include mySystem
    include emailService
  }
}
```

**Do not** put step-by-step sequences in C1. If the request sounds like “first the user does X, then the webapp does Y”, that belongs in `views 'Use Cases'`.

## Step 2 — C2 Containers

Once the system boundary is clear, break the system into **runtime units**.

```likec4
model {
  mySystem = System_Existing 'My System' {
    webapp = Container_Webapp 'Web Application' {
      technology 'React, TypeScript'
      description 'Single-page application providing the user interface'
    }

    api = Container_Api 'API Server' {
      technology 'Node.js, Express'
      description 'RESTful API handling business logic'
    }

    database = Container_Database 'Database' {
      technology 'PostgreSQL 15'
      description 'Stores application data and user information'
    }
  }

  user -[calls]-> mySystem.webapp 'Interacts with'
  mySystem.webapp -[calls]-> mySystem.api 'Makes API requests'
  mySystem.api -[reads]-> mySystem.database 'Queries data'
  mySystem.api -[writes]-> mySystem.database 'Persists data'
}
```

**Container test:** if it must be running as a distinct runtime boundary for the system to work, it is a candidate container. If it is just code organization inside a container, it is not.

Use `design-view` to build the C2 view once the container set is stable.

## Step 3 — C3 Components, Selectively

Do **not** create a C3 view for every container. Create C3 only for containers that are:

- architecturally central
- risky or difficult to reason about
- internally complex enough that C2 is no longer explanatory

```likec4
model {
  mySystem = System_Existing 'My System' {
    api = Container_Api 'API Server' {
      technology 'Node.js, Express'
      description 'RESTful API handling business logic'

      routing = Component 'Routing' {
        technology 'Express Router'
        description 'Maps incoming requests to handlers'
      }

      auth = Component 'Authentication' {
        technology 'JWT'
        description 'Validates identity and permissions'
      }

      application = Component 'Application Services' {
        technology 'TypeScript'
        description 'Runs core business use cases'
      }
    }
  }

  mySystem.api.routing -[uses]-> mySystem.api.auth 'Validates access'
  mySystem.api.routing -[uses]-> mySystem.api.application 'Delegates work'
}
```

**Component rule:** components are **logical code groupings**, not deployable units.

If a container is simple and well understood from C2, stop at C2.

## Step 4 — Dynamic Views (Optional, After C2)

Dynamic views are for **time-ordered behavior**, not structure.

- place them in `views 'Use Cases'`
- use plain `->` arrows
- start with the initiating actor/system
- create them only for workflows worth explaining

```likec4
views 'Use Cases' {
  dynamic view request_flow {
    title 'User Request Flow'

    user -> mySystem.webapp 'Opens page'
    mySystem.webapp -> mySystem.api 'Requests data'
    mySystem.api -> emailService 'Sends notification'
  }
}
```

Use `create-sequence-view` for the detailed dynamic-view rules.

## Step 5 — Deployment Views (Optional, After Structure Stabilizes)

Deployment answers **where it runs**, not **what the system is**.

```likec4
deployment {
  prod = Node_Environment 'Production' {
    appTier = Zone 'Application Tier' {
      apiVm = Node_Vm 'prod-api-vm' {
        technology 'Docker on Ubuntu'
        description 'Hosts the API runtime'

        apiApp = Node_App 'API App' {
          instanceOf mySystem.api
        }
      }
    }
  }
}
```

Use `model-deployment-infrastructure` for naming, hierarchy, rich descriptions, and `instanceOf` rules.

## View Organization

Use category folders consistently. The root `index` view is the only common exception.

```likec4
views {
  view index extends c1_context {}
}

views 'C1' {
  view c1_context { }
}

views 'C2' {
  view c2_containers { }
}

views 'C3' {
  view c3_api { }
}

views 'Use Cases' {
  dynamic view request_flow { }
}

views 'Deployment' {
  deployment view prod_overview { }
}
```

**Important:**
- `C3` is optional — create it only if you actually need component detail
- `Use Cases` is optional — create it only for meaningful flows
- `Deployment` is optional — create it only when topology matters

## Handoff Rules

This skill decides **what comes next**. The detailed work belongs to more specific skills.

- unfamiliar workspace or unknown kinds → `understand-project-structure`
- creating or changing elements → `create-element`
- choosing relationship kinds/labels → `create-relationship`
- building static views → `design-view`
- documenting runtime flows → `create-sequence-view`
- modeling environments/zones/VMs → `model-deployment-infrastructure`
- validating integrity/rendering → `test-model`

## Common Mistakes

❌ Starting from classes, folders, or frameworks  
✅ Start from system boundary, then runtime containers, then selected components

❌ Treating every container as if it needs a C3 view  
✅ Create C3 only where extra internal detail improves understanding

❌ Putting temporal flows in C1  
✅ Keep C1 static; move temporal behavior to `views 'Use Cases'`

❌ Using this skill to do every detailed edit itself  
✅ Use it as the orchestration layer, then hand off to specialized skills

❌ Jumping to deployment before the logical model exists  
✅ Stabilize C1/C2 first, then add deployment if runtime topology matters

## Done Criteria

- C1 boundary is clear
- C2 explains the main runtime structure
- C3 exists only where it adds real value
- dynamic and deployment views are added only when justified
- the next detailed edit is delegated to the right specialized skill
- `test-model` can validate the result before commit
