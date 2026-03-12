Use the **external integration** pattern.

In this workspace, the consistent structure is:

```likec4
api = Container_Api 'Payments API' {
  technology 'Node.js'
}

paymentProvider = System_External 'Payment Provider' {
  technology 'REST API'
  description 'Third-party payment processor'
  #External
}

api -[calls]-> paymentProvider 'Process payment' {
  technology 'HTTPS'
}
```

Keep these guardrails:

- Model the provider as its own `System_External` and keep the shared `#External` tag.
- Use a typed `-[calls]->` relationship from the internal API to the external system.
- Make the label action-focused, such as `Process payment`, instead of something vague like `Integration call`.
- Put the interaction technology on the relationship (`HTTPS` here), not in the label.
