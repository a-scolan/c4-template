Relationship choice: move normal browser/application traffic back to the system model; do not keep `Prod.Web.webApp -[https]-> Prod.App.apiApp` in deployment unless it represents an infrastructure-only exception.
Short rule: In this repository, normal app traffic belongs in the logical model with a model relationship kind plus `technology '...'`. Deployment relationships such as `https` are reserved for infra-only cases like monitoring scrapes, replication, bastion access, or storage mounts. Deployment instances should inherit the logical relationships through `instanceOf`.
Minimal example:
user -[calls]-> webApp 'Uses UI' {
  technology 'Manual'
}
webApp -[calls]-> api 'Sends request' {
  technology 'HTTPS'
}
api -[calls]-> internalService 'Routes request' {
  technology 'HTTP/8080'
}
Use `Manual` for human interaction, `HTTPS` for normal browser/service traffic, and `HTTP/8080` only when you need to show a non-default port.
Counter-example / anti-pattern:
Prod.Web.webApp -[https]-> Prod.App.apiApp
That duplicates normal application traffic in deployment instead of letting the deployment instances inherit it from the system model.
