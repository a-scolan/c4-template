# Real Payment API vs Mock Variant — Two Elements, One Kind

**Use two elements of the same kind**, not two kinds.

## Why Not Two Kinds

The skill explicitly says:
> "Invent `Container_MockApi` just to distinguish a test double from production → **Bad decision**"

Mock vs prod is a **runtime concern**, not a structural distinction. The structural shape (API container) is the same for both.

## Declaration

```likec4
model {
  paymentSystem = System_New 'Payment System' {

    paymentApi = Container_Api 'Payment API' {
      technology 'Java, Spring Boot'
      description 'Processes real payment transactions via the payment gateway.'
    }

    paymentApiMock = Container_Api 'Payment API Mock' {
      technology 'Node.js, WireMock'
      description 'Stub of the payment API used in integration test environments.'
    }

  }
}
```

## Which Skill Handles Mock vs Prod Placement?

Routing mock vs prod to different environments (e.g., `test` vs `prod` deployment nodes) is a **deployment concern** — use **`model-deployment-infrastructure`** to place each element instance in the appropriate environment.
