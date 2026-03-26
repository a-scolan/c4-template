# virusScanProvider + scanApi + Arrows + C2 View — Skill Map

The skill guidance is clear: lead with element declarations, then hand off the rest.

## 1. Elements (This Skill — `create-element`)

```likec4
model {
  virusScanProvider = System_External 'Virus Scan Provider' {
    technology 'HTTPS API'
    description 'Third-party malware detection service integrated before file acceptance.'
  }

  ingestionSystem = System_New 'Ingestion System' {

    scanApi = Container_Api 'Scan API' {
      technology 'Node.js'
      description 'Internal container that proxies scan requests to the external virus scan provider.'
    }

  }
}
```

## 2. Arrows → `create-relationship`

Use `create-relationship` to add the outgoing relationship from `scanApi` to `virusScanProvider`.

## 3. C2 View → `design-view`

Use `design-view` to create the container-level view with `ingestionSystem` as parent context, including `scanApi` and its neighbors.

**Summary:** elements here → arrows to `create-relationship` → C2 view to `design-view`.
