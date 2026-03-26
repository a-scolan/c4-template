# virusScanProvider, scanApi, Arrows, and C2 View

The skill rule is: **answer with declarations first**, route the rest.

## Element Declarations

```likec4
model {
  // External system — C1 level
  virusScanProvider = System_External 'Virus Scan Provider' {
    technology 'HTTPS API'
    description 'Third-party malware scanning service called before accepting uploaded files.'
  }

  uploadSystem = System_New 'Upload System' {

    // Internal container — C2 level
    scanApi = Container_Api 'Scan API' {
      technology 'Node.js, Fastify'
      description 'Submits file hashes to the external virus scan provider and enforces the accept/reject verdict.'
    }

  }
}
```

## Skill Routing

- **Arrows** (e.g., `scanApi -> virusScanProvider`) → use **`create-relationship`**
- **C2 container view** showing `scanApi` and neighbors → use **`design-view`**

This skill covers element declaration only; relationship definition and view design each have their own dedicated skill.
