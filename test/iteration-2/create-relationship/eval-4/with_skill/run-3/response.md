# Eval 4 — Deployment `https` for browser traffic: keep or remove?

## 1. Relationship choice

**Remove it from deployment.** Express this connection in the logical model with `calls` and a `technology` field.

## 2. Rule

Deployment relationship kinds (`http`, `https`, `tcp`, `nfs`, `amqp`, …) are reserved for infrastructure-only facts that the logical model does **not** already express: monitoring scrapes, storage mounts, replication channels, bastion SSH hops. Normal application traffic — a web app calling an API — is a logical concern and belongs in the system model.

`Manual`, `HTTPS`, and `HTTP/8080` are **technology values**, not relationship kinds. They always go inside `technology '...'` within a model relationship block.

## 3. Correct placement (logical model)

```likec4
user -[calls]-> webApp 'Uses UI' {
  technology 'Manual'
}

webApp -[calls]-> api 'Sends request' {
  technology 'HTTPS'
}

api -[calls]-> internalService 'Routes request' {
  technology 'HTTP/8080'
}
```

## 4. Anti-pattern

```likec4
// ❌ Wrong: duplicating normal app traffic in deployment
Prod.Web.webApp -[https]-> Prod.App.apiApp 'Browser traffic'

// ❌ Wrong: protocol as relationship kind in logical model
webApp -[https]-> api 'Sends request'
```

## 5. Summary — where each value lives

| Value | Where it belongs |
|---|---|
| `calls` | Inline model relationship kind |
| `async`, `reads`, `writes` | Inline model relationship kind |
| `HTTPS`, `HTTP/8080`, `Manual`, `AMQP` | `technology '...'` field in model block |
| `https`, `tcp`, `nfs` (deployment kinds) | Deployment file, infrastructure-only hops only |
