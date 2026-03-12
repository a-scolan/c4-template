Model this as an **external integration with two explicit interactions**, not as one request with an implied return.

First, represent Stripe as a dedicated external system:

`stripe = System_External 'Stripe' { technology 'REST API + Webhooks'; description 'External payment provider'; #External }`

Then model the outbound payment creation call:

`vault.api -[calls]-> stripe 'Create payment'`

Model the webhook as a second, separate interaction:

`stripe -[calls]-> vault.api 'Payment confirmation webhook'`

That separation matters: the webhook is **not** a synchronous return from the first relationship. It is a new inbound call initiated later by Stripe.

If you need to show the temporal order in more detail, you can complement the structural model with **`create-sequence-view`**.