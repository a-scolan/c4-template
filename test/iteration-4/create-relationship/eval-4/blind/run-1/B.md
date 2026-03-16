Usually no. The cheat sheet says deployment relationships are for infrastructure-specific connections, while normal application traffic should usually be modeled in the system model and inherited in deployment through instanceOf. So do not keep Prod.Web.webApp -[https]-> Prod.App.apiApp in deployment just to show ordinary browser or app traffic.
Manual, HTTPS, and HTTP/8080 belong on the system-model relationship as technology values, for example:
user -[uses]-> webApp 'Uses UI' {
  technology 'Manual'
}
webApp -[calls]-> apiApp 'Calls API' {
  technology 'HTTPS'
}
legacyClient -[calls]-> apiApp 'Calls API' {
  technology 'HTTP/8080'
}
Use the port only when it is non-default for the protocol. Keep a deployment -[https]-> relationship only when you are modeling an infrastructure-specific connection.
