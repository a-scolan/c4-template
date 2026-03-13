1. probable error category: wrong-scope relationship taxonomy in `model {}` plus duplicated deployment edge.
2. root cause: `https` is a deployment relationship type, but you used it in the logical system model. Then the same application traffic was redrawn again between deployed apps, which duplicates behavior that should already be inherited through `instanceOf`.
3. verification step: confirm in `projects/shared/spec-deployment.c4` that `https` is defined under deployment relationships, and in `projects/shared/spec-global.c4` that the logical model should use kinds such as `calls`. Then check whether the deployed apps already use `instanceOf` to map back to the model elements; if they do, the logical relationship propagates automatically.
4. minimal fix: keep the traffic once in the system model with a logical relationship kind and put the protocol in `technology`, then delete the duplicate deployment edge.

Corrected model edge:
`webapp -[calls]-> api 'Browser traffic' { technology 'HTTPS' }`

Deployment fix:
keep the `instanceOf` mapping, but remove the extra `webappApp -[https]-> apiApp` relationship.
