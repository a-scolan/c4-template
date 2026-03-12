Do not create two kinds.

Reuse the same existing workspace kind for both logical APIs, and only split them into two elements if they are genuinely different services with different responsibilities or lifecycle.

For example, if they are distinct logical services, model them as two elements of the same kind:

```likec4
paymentApi = Container_Api 'Payment API' {
  technology 'HTTPS'
  description 'Production payment integration used in live flows'
}

mockPaymentApi = Container_Api 'Mock Payment API' {
  technology 'WireMock'
  description 'Test double used by integration tests'
}
```

Do not invent something like `Container_MockApi`.

If the difference is only environment-specific behavior, keep one logical element and represent mock vs production with deployment modeling and/or dedicated views. If you need the model to make the distinction visible, use tags or view scoping rather than a special kind.