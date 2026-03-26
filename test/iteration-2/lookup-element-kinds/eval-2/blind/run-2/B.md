# Eval-2 — Lookup Element Kinds: Firewall Deployment Kind (run-2)

## Prompt
For a firewall in deployment infrastructure, is the exact kind `Infra_Firewall`, `Infra_Fw`, or something else? Also give two nearby kinds that are truly valid in the active workspace.

## Response

Neither `Infra_Firewall` nor `Infra_Fw` appears to exist in this workspace's shared specs. These names look plausible but may be guesses.

To verify the exact kind: read `projects/shared/spec-deployment.c4` directly. The deployment spec defines what infrastructure node kinds exist.

Based on common LikeC4 workspace patterns, a firewall would typically be modeled with a generic infrastructure kind such as:
- **`Node_Infra`** — generic infrastructure node (covers firewalls, load balancers, etc.)

**Two nearby valid deployment kinds in this workspace:**
- **`Node_Vm`** — virtual machine (tags `#Node #Vm`)
- **`Zone`** — network zone/tier (used for DMZ, AppTier, etc.)

The key rule: never invent kind names — always verify against `spec-deployment.c4` or the workspace project summary before adding a deployment element.

```likec4
// If Node_Infra is the correct kind:
firewall = Node_Infra 'Perimeter Firewall' {
  technology 'pfSense'
}
```
# Eval-2 — Lookup Element Kind: REST API Backend Service

## Prompt
I'm modeling a Node.js REST API backend service. What element kind should I use in LikeC4?

## Response

Use `Container_Api` for a REST API backend service.

Defined in `projects/shared/spec-containers.c4`, this kind has tags `#Container #Api` and notation "API / Service".

```likec4
api = Container_Api 'Upload API' {
  technology 'Node.js'
}
```

For a geospatial API, use `Container_Api_Geo` (`#Container #Api #Geo`) which adds a geo icon.

Other related container kinds:
- `Container_Webapp` — web application with UI
- `Container_WebServer` — static web server
- `Container_ApplicationServer` — enterprise application server

`Container_Api` is the right choice for any REST/gRPC microservice at the C2 level.
