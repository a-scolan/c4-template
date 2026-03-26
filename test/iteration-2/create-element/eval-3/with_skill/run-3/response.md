# Payment API + Mock: Two Elements, Same Kind

**Two elements of the same kind is the right answer.**

## Reasoning

Structural shape is the same for both: both are HTTP API containers. The only difference is purpose (production vs test). The skill is explicit:
> "Use two elements of the same kind when responsibilities differ (e.g., prod vs mock API)"  
> Creating `Container_MockApi` for a test double → *bad decision*

## Minimal Declarations

```likec4
model {
  paymentSystem = System_New 'Payment System' {

    paymentApi = Container_Api 'Payment API' {
      technology 'Java, Spring Boot'
      description 'Handles live payment transactions through the payment provider gateway.'
    }

    paymentApiMock = Container_Api 'Payment API Mock' {
      technology 'Node.js, MockServer'
      description 'Simulates payment API responses for integration and regression test runs.'
    }

  }
}
```

## Skill for Mock vs Prod Separation

Separating mock from prod across deployment environments → **`model-deployment-infrastructure`**.  
To avoid deploying the mock to production, model environment-specific deployment nodes there.
