# Eval-4 — Lookup Element Kinds: https vs calls (run-2)

## Prompt
For a web application talking to an API in the logical model, should the relationship kind be `https` or `calls`? And when does `https` become valid in the active workspace?

## Response

In the **logical model** (`model {}` block), use **`calls`** — not `https`.

`https` is a **deployment-level** relationship kind. It encodes transport protocol, which belongs in the deployment section (or in the `technology` field of a logical relationship).

**Rule:**
- Logical model → use `calls` with `technology 'HTTPS'` if you want to document the protocol
- Deployment model → use `-[https]->` between deployed instances

```likec4
// ✅ Correct — logical model
webApp -[calls]-> api 'Browse files' {
  technology 'HTTPS'
}

// ❌ Wrong — https used in logical model
webApp -[https]-> api 'Browse files'

// ✅ Correct — deployment model
Prod.Dmz.WebVm -[https]-> Prod.AppTier.ApiVm 'Route requests'
```

**When `https` becomes valid:** only inside a `deployment {}` block (or in deployment relationships in `deployment.c4`), where relationship kinds from `spec-deployment.c4` apply. Check that spec file for the full list of valid deployment relationship kinds.
# Eval-4 — Lookup Element Kind: Message Queue

## Prompt
My system uses RabbitMQ for asynchronous job processing. What element kind should I use in LikeC4?

## Response

Use `Container_Queue` for a message queue like RabbitMQ.

From `projects/shared/spec-containers.c4`: tags `#Container #Queue`, shape `queue`, icon mailbox.

```likec4
queue = Container_Queue 'Job Queue' {
  technology 'RabbitMQ'
}
```

The `#Queue` tag also exists as a global technology tag in `spec-global.c4` with amber color, providing extra visual differentiation.

For async communication with the queue, use the `async` relationship:
```likec4
api -[async]-> queue 'Publishes job' {
  technology 'AMQP'
}
worker -[async]-> queue 'Consumes job' {
  technology 'AMQP'
}
```
