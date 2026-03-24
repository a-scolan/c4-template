Use two elements of the same existing kind, not two new kinds. The workspace rule is to reuse shared kinds and distinguish mock vs. prod with element names, titles, and descriptions.

For a vendor payment integration, that usually means two `System_External` elements:

paymentProvider = System_External 'Payment Provider' {
  technology 'HTTPS API'
  description 'Production payment provider used for real transactions.'
}

mockPaymentProvider = System_External 'Mock Payment Provider' {
  technology 'HTTP test double'
  description 'Integration-test stub that mimics the production payment provider.'
}

If both live inside your own system boundary instead, use two `Container_Api` elements rather than inventing kinds like `Container_MockApi`. `create-element` handles choosing the correct kind and declaring both elements; if you later need to show who calls mock vs. prod, that becomes a `create-relationship` task.
