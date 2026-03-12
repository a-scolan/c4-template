Model this as two separate interactions: one outbound API call and one inbound webhook.

```likec4
stripe = System_External 'Stripe' {
  technology 'Stripe API'
  description 'External payment provider'
}

vault.api -[calls]-> stripe 'Create payment'
stripe -[calls]-> vault.api 'Send payment confirmation webhook'
```

This keeps the provider as a dedicated external system and makes both directions explicit:

- `vault.api -> stripe` is the outbound request to create the payment.
- `stripe -> vault.api` is a second, separate interaction for the webhook callback.

Do not model the webhook as an implicit return of the first relationship, because that would suggest synchronous request/response behavior. The confirmation arrives later as a distinct inbound event.

If you need to show the exact temporal order in more detail, add a separate sequence view.