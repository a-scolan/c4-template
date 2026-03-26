# Eval 0 — Connect web application to API container

## 1. Relationship choice

Use **`calls`**.

## 2. Rule

Service-to-service synchronous invocation uses `calls`. The relationship kind is placed inline in the arrow syntax (`-[calls]->`). Protocol or medium details go in the `technology '...'` field inside the block. Never put the kind keyword inside the block.

## 3. Minimal example

```likec4
webApp -[calls]-> api 'Sends request' {
  technology 'HTTPS'
}
```

## 4. Anti-pattern

```likec4
// ❌ Wrong: relationship kind belongs inline, not inside the block
webApp -> api {
  calls 'Sends request'
  technology 'HTTPS'
}

// ❌ Wrong: no kind specified at all
webApp -> api 'Sends request'
```

## 5. Where it belongs

This relationship belongs in the **`model {}`** section of your **logical model file** — not in a deployment file. Deployment relationships (`http`, `https`, `tcp`, …) are reserved for infrastructure-only connections not already expressed in the logical model.
