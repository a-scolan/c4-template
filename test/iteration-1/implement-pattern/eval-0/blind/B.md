Use the **external integration** pattern.

Add a dedicated external system for the payment provider and tag it as external:

`paymentProvider = System_External 'Payment Provider' { technology 'REST API'; description 'External payment processor'; #External }`

Then connect your internal API with a typed `calls` relationship:

`vault.api -[calls]-> paymentProvider 'Process payment'`

Keep the relationship label action-focused, such as **`Process payment`**, rather than something vague like `Integration` or `Request`.