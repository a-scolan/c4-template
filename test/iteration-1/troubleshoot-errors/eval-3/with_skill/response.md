1. Probable error category: wrong relationship scope + duplicate deployment modeling.
2. Root cause: inside `model {}`, `https` was used as if it were a logical relationship kind. In this workspace, protocol belongs in the `technology` field, while the logical relationship kind should be something like `calls`. Then the same application traffic was redrawn again between deployed apps, even though deployment usually inherits that traffic through `instanceOf`.
3. Verification step: check the shared relationship definitions. Model kinds are `uses`, `calls`, `async`, `reads`, and `writes`; deployment kinds like `https` are for infrastructure-specific deployment links. Also confirm the deployed apps already point to the model elements with `instanceOf`.
4. Minimal fix: keep one logical relationship in the system model and move the protocol into `technology`; delete the duplicate deployment edge unless it represents infrastructure-only connectivity.
Correct model snippet:
`webapp -[calls]-> api 'Browser traffic' { technology 'HTTPS' }`
Clean deployment approach:
`webappApp { instanceOf corePlatform.webapp }`
`apiApp { instanceOf corePlatform.api }`
Do not add `webappApp -[https]-> apiApp` again unless you are modeling a deployment-specific path that does not already exist in the logical model.
