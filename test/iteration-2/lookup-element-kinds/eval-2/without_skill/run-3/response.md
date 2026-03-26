# Eval-2 — Lookup Element Kinds: Firewall Deployment Kind (run-3)

## Prompt
For a firewall in deployment infrastructure, is the exact kind `Infra_Firewall`, `Infra_Fw`, or something else? Also give two nearby kinds that are truly valid in the active workspace.

## Response

`Infra_Firewall` and `Infra_Fw` are NOT confirmed to exist in this workspace. You should check the spec file directly before using any deployment kind.

**How to verify:** Read `projects/shared/spec-deployment.c4` and look for the `specification { deploymentNodeKinds }` section. If no `Infra_Firewall` or `Infra_Fw` appears there, those names are invalid.

A firewall is typically generic infrastructure; use the most generic available deployment infrastructure kind. In many LikeC4 workspaces, that is `Node_Infra`.

**Two nearby valid kinds in this workspace (from spec-deployment.c4):**
- **`Node_Vm`** — virtual machine host (`#Node #Vm`)
- **`Node_App`** — deployed application instance within a VM (`#Node #App`)

These definitely exist. For a firewall specifically:
- Check if `Infra_Firewall` or `Node_Infra` are declared; if not, use the closest available kind or add the kind to the spec.

```likec4
// After confirming the correct kind in spec-deployment.c4:
pfwVm = Node_Vm 'pfw-vm' {
  technology 'pfSense'
  // instanceOf: depends on what's in the logical model for the firewall
}
```
# Eval-2 — Lookup Element Kind: REST API Backend Service

## Prompt
I'm modeling a Node.js REST API backend service. What element kind should I use in LikeC4?

## Response

Use `Container_Api` for a REST API backend service.

From `projects/shared/spec-containers.c4`: tags are `#Container #Api`, notation is "API / Service", with a server icon.

```likec4
api = Container_Api 'Upload API' {
  technology 'Node.js'
}
```

Geo-specific variant: `Container_Api_Geo` (`#Container #Api #Geo`).

Related kinds for server-type containers:
- `Container_Webapp` — web app with server-rendered UI
- `Container_ProcessingServer` — batch/background processing
- `Container_WebServer` — static file serving

`Container_Api` is the standard c2-level kind for service-oriented backends and microservices.
