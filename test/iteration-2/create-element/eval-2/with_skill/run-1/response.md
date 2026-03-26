# Adding `virusScanProvider` and `scanApi` + Arrows + C2 View

Per skill guidance: **provide element declarations first**, then route other concerns to the right skill.

## Element Declarations (This Skill)

```likec4
model {
  virusScanProvider = System_External 'Virus Scan Provider' {
    technology 'HTTPS API'
    description 'Third-party malware scanning service used before file acceptance.'
  }

  uploadSystem = System_New 'Upload System' {

    scanApi = Container_Api 'Scan API' {
      technology 'Node.js, Fastify'
      description 'Internal adapter that submits files to the virus scan provider and returns the verdict.'
    }

  }
}
```

## Skill Routing for the Rest

| Concern | Skill |
|---|---|
| Relationship arrows (`scanApi → virusScanProvider`) | `create-relationship` |
| C2 container view showing `scanApi` and its context | `design-view` |
