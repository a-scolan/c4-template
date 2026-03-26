# Eval-4 — Lookup Element Kinds: https vs calls (run-3)

## Prompt
For a web application talking to an API in the logical model, should the relationship kind be `https` or `calls`? And when does `https` become valid in the active workspace?

## Response

**Use `calls` in the logical model.** The `https` relationship kind is valid only in the deployment model.

**Why:**
- `calls` is defined in the model relationship kinds (spec-global.c4) — it represents a synchronous invocation between logical elements
- `https` is a deployment relationship kind — it encodes the transport layer protocol between physical/virtual nodes

Mixing deployment kinds into the logical model breaks the C4 separation: the logical model describes WHAT communicates, the deployment model describes HOW (protocol, port).

**For protocol documentation in the logical model:**
```likec4
webApp -[calls]-> api 'Makes API requests' {
  technology 'HTTPS'   // ← protocol goes in technology field, NOT as relationship kind
}
```

**`https` is valid** once you're inside a `deployment {}` block using deployment-level relationship kinds from `spec-deployment.c4`:
```likec4
// deployment.c4
Prod.Dmz.webApp -[https]-> Prod.App.api 'Browser traffic'
```

Tags summary: `calls` has no special display tags; it renders as a solid blue arrow in the logical model.
# Eval-4 — Lookup Element Kind: Message Queue

## Prompt
My system uses RabbitMQ for asynchronous job processing. What element kind should I use in LikeC4?

## Response

Use `Container_Queue` for a message queue like RabbitMQ.

In `projects/shared/spec-containers.c4`, `Container_Queue` has tags `#Container #Queue` and uses a `queue` shape with a mailbox icon.

```likec4
queue = Container_Queue 'Job Queue' {
  technology 'RabbitMQ'
}
```

Notable: `#Queue` is also declared as a global tag in `spec-global.c4` with amber color. This makes queue-type containers visually distinct in diagrams.

The recommended relationship kind for messaging is `async` (dashed blue line):
```likec4
api -[async]-> queue 'Publishes job' {
  technology 'AMQP'
}
```

There is no direct sub-variant of `Container_Queue` — it covers all broker-based messaging systems (RabbitMQ, ActiveMQ, Kafka-style queues, etc.).
