Relationship choice: do not keep `Prod.Web.webApp -[https]-> Prod.App.apiApp` in deployment just to show normal browser traffic.
Rule: Normal application traffic belongs in the logical system model with a model relationship kind such as `calls`, plus `technology '...'`. Deployment relationships are for infrastructure-only exceptions that the logical model does not already express.
Example:
user -[calls]-> webApp 'Uses UI' {
  technology 'Manual'
}
webApp -[calls]-> api 'Sends request' {
  technology 'HTTPS'
}
api -[calls]-> internalService 'Routes request' {
  technology 'HTTP/8080'
}
Anti-pattern:
Prod.Web.webApp -[https]-> Prod.App.apiApp 'Browser traffic'
`Manual`, `HTTPS`, and `HTTP/8080` should live as `technology` values on those logical-model relationships, not as the primary reason to duplicate normal app traffic in deployment.
