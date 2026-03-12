---
name: create-element
description: Use when creating or modifying LikeC4 elements (systems, containers, components, nodes) with proper naming conventions, required metadata, and correct C4 hierarchy placement.
---

# Create LikeC4 Element

## Goal

Answer with a usable, repo-aligned declaration first.

Default flow:
1. choose the exact declared kind
2. place it under the right parent
3. show the smallest valid snippet
4. add only the extra fields or handoffs the user actually needs

If the user asks “what should I model?”, do **not** respond with routing alone when you can already give the declaration.

## When to Use

- Creating a new system, container, component, or deployment node
- Modifying `technology`, `description`, tags, links, icons, or metadata
- Checking whether an existing shared kind fits before proposing a new one
- Distinguishing “new element” from “new kind”

**Do not use** for relationship arrows or view design — use `create-relationship` and `design-view`.

If the system boundary itself is still unclear, hand off to `c4-modeling-process` **after** giving the minimal element recommendation.

## Local source of truth

Check these in this order:

1. active project summary (`read-project-summary`) or the project config/model files
2. `projects/shared/SPEC_CHEATSHEET.md`
3. `projects/shared/spec-context.c4`, `spec-containers.c4`, `spec-components.c4`, `spec-deployment.c4`
4. existing project model files for placement and naming consistency

Example projects help with inspiration, but they are **not** the semantic source of truth for kinds or tags.

## Default response shape

When the prompt is concrete, answer in this order:

1. **Recommended kind + parent**
2. **Minimal declaration**
3. **Optional enrichments** (`tag`, `link`, `icon`, metadata)
4. **Follow-up skill** only if the user is now moving to arrows, views, descriptions, or deployment

## Common declared kinds in this repository

| Layer | Typical kinds used here |
|---|---|
| Context | `Actor_Person`, `Actor_Staff`, `Actor_Admin`, `System_New`, `System_Existing`, `System_Legacy`, `System_External` |
| Containers | `Container_Api`, `Container_Webapp`, `Container_Queue`, `Container_Database`, `Container_ObjectStorage`, `Container_Directory`, `Container_Loadbalancer`, `Container_FileServer` |
| Components | `Component` |
| Deployment | `Node_Environment`, `Zone`, `Node_Vm`, `Node_App`, `Infra_Fw` |

Use the exact shared spelling/case. For example: `Container_Api`, **not** `Container_API`.

## Direct answer first, handoff second

### Canonical internal container example

```likec4
model {
  ingestionApi = Container_Api 'Ingestion API' {
    technology 'Node.js, Fastify'
    description 'Receives uploaded files and starts the ingestion workflow.'
  }
}
```

### Canonical external system example

```likec4
model {
  virusScanProvider = System_External 'Virus Scan Provider' {
    technology 'HTTPS API'
    description 'Third-party malware scanning service used before file acceptance.'
  }
}
```

If the prompt also asks for arrows or views, still lead with the element declarations, then route:
- arrows → `create-relationship`
- C1/C2/C3/deployment views → `design-view`
- richer descriptive blocks/tables → `write-rich-descriptions`
- deployment/runtime placement → `model-deployment-infrastructure`

## Core rules

| Topic | Rule |
|---|---|
| Kind naming | Exact declared `Category_Subtype` PascalCase (`Container_Api`, `Node_Vm`) |
| Variable naming | camelCase (`ingestionApi`, `prodUploadVm`) |
| Description | Required for all elements; explain purpose and responsibilities |
| Technology | Expected for systems/containers/components/nodes when it is known; always include it for containers, components, and deployment nodes |
| Tags | Reuse declared tags with exact spelling/case only when they add operational meaning beyond the kind |
| Metadata | Optional; add only if someone will filter/query it |
| Hierarchy | `System → Container → Component` and `Environment → Zone → VM → App` |
| New kinds | Last resort only; check shared specs first and ask before introducing one |

## Shared-spec-first rule

Prefer an existing shared kind over a one-off local kind.

### Good decisions
- use `Container_Api` for a new internal API
- use `System_External` for a vendor platform
- use two elements of the same kind when responsibilities differ (for example prod vs mock API)

### Bad decisions
- invent `Container_UploadOrchestrator` for a single service when `Container_Api` or another declared kind already fits
- invent `Container_MockApi` just to distinguish a test double from production
- create project-local kinds that should really live in shared specs

## Enrichment patterns

### Multi-line description

```likec4
model {
  ingestionApi = Container_Api 'Ingestion API' {
    technology 'Node.js, Fastify'
    description """
      Receives upload requests and starts the ingestion workflow.

      **Responsibilities:**
      - validate upload metadata
      - persist accepted jobs for downstream processing
    """
  }
}
```

### Links and icons

```likec4
model {
  primaryDatabase = Container_Database 'Primary Database' {
    technology 'PostgreSQL 15'
    description 'Stores canonical application data.'
    icon tech:postgresql
    link https://www.postgresql.org/docs/ 'PostgreSQL documentation'
  }
}
```

Use icon namespaces such as `tech:`, `aws:`, `gcp:`, `azure:` only when they help the view.

## Validation checklist

- [ ] Exact kind reused from shared specs
- [ ] Variable is camelCase
- [ ] Parent hierarchy is correct
- [ ] Description explains purpose, not just type
- [ ] Technology is present for containers/components/deployment nodes
- [ ] Tags keep exact shared spelling/case when reused
- [ ] Metadata is present only if it serves querying/automation

## If MCP is unavailable

Stay useful anyway:

1. inspect `projects/shared/SPEC_CHEATSHEET.md` and `projects/shared/spec-*.c4`
2. inspect the active project `likec4.config.json` and nearby model files
3. recommend the exact kind and give the minimal snippet immediately
4. list the checks to run later once MCP is back (`read-project-summary`, `search-element`, `read-element`)

Do **not** become generic just because MCP is unavailable; use the repository taxonomy you can already see.

## Context7 validation

Use Context7 `/likec4/likec4` only when syntax remains unclear after reading local files, especially for:
- property syntax (`technology`, `description`, `link`, `icon`)
- Markdown description formatting
- uncommon element-property combinations

## Common mistakes

❌ guessed kinds such as `Container_API`, `Component_Service`, `Node_VM`

❌ answering only with “use another skill” when a minimal declaration is already possible

❌ creating a new kind instead of reusing an existing shared kind

❌ using tags to repeat what the kind already says

❌ placing containers outside their system or apps outside their VM hierarchy

## Output

Return a concrete declaration that is ready to paste, with minimal but sufficient documentation and the correct parent placement.
