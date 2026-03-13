Use two elements of the same existing kind, not two kinds. In this workspace, the default answer is two `Container_Api` elements, for example:
paymentApi = Container_Api 'Payment API' {
  technology 'Node.js, Fastify'
  description 'Calls the real payment provider for live payment operations.'
}
paymentApiMock = Container_Api 'Payment API Mock' {
  technology 'WireMock'
  description 'Test double used by integration tests to emulate payment API behavior.'
}
Do not create `Container_MockApi`. Distinguish mock vs prod at the element level by naming and, if your workspace already has a suitable shared tag, by reusing that tag; otherwise use a dedicated integration-test view. If the difference is really about runtime environments or placement, use `model-deployment-infrastructure`, and use `design-view` for the view-level distinction.
