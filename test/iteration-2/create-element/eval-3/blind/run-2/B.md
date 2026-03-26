# Real Payment API + Mock Variant

**Answer: two elements, same kind.**

## The Rule

The skill explicitly covers this case:
> "Use two elements of the same kind when responsibilities differ (for example prod vs mock API)"
> "Invent `Container_MockApi` just to distinguish a test double → **Bad decision**"

Two kinds would fragment the shared taxonomy for no gain; two elements with clear names communicate intent properly.

## Declarations

```likec4
model {
  paymentSystem = System_New 'Payment System' {

    paymentApi = Container_Api 'Payment API' {
      technology 'Java, Spring Boot'
      description 'Processes real-money transactions through the external payment gateway.'
    }

    paymentApiMock = Container_Api 'Payment API Mock' {
      technology 'Node.js, Hoverfly'
      description 'Test double simulating payment API responses for integration test environments.'
    }

  }
}
```

## Deployment Difference

The difference between mock and prod is a **deployment/environment** concern, not a model kind distinction. Use **`model-deployment-infrastructure`** to place each element in the appropriate environment (`test` vs `prod`).
