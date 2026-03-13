Usually no. Do not keep `Prod.Web.webApp -[https]-> Prod.App.apiApp` in deployment just to show normal application traffic; model that in the system model and let deployment inherit it through `instanceOf`. `Manual`, `HTTPS`, and `HTTP/8080` belong in the system-model relationship `technology` field, for example:
user -[calls]-> webApp 'Uses UI' {
  technology 'Manual'
}
webApp -[calls]-> api 'Calls API' {
  technology 'HTTPS'
}
webApp -[calls]-> api 'Calls API' {
  technology 'HTTP/8080'
}
Keep deployment relationships only for infrastructure-specific links such as ingress or node-to-node wiring.
