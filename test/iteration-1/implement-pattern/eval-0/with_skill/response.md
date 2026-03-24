Pattern: External integration.

Minimal scaffold:
paymentProvider = System_External 'Payment Provider' {
  technology 'HTTPS API'
  description 'External payment service used by the platform.'
}

api -[calls]-> paymentProvider 'Creates payment / checks status' {
  technology 'HTTPS'
}

Substitute before finalizing:
- parent: place `paymentProvider` at the correct external/system level next to your internal `api`
- exact kinds: replace `System_External` or `calls` if your workspace declares different names
- names: use the real provider name, for example `stripe`
- tech: keep the element technology as the provider API and the relationship technology as the transport, usually `HTTPS`

Keep the provider modeled as external, not as an internal container.
