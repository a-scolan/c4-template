No — remove `Prod.Web.webApp -[https]-> Prod.App.apiApp` from deployment. Normal application traffic should be modeled once in the logical system model, and deployment instances should inherit it via `instanceOf`.

```likec4
user -[calls]-> mySystem.webapp 'Uses UI' {
  technology 'Manual'
}

mySystem.webapp -[calls]-> mySystem.api 'Makes API requests' {
  technology 'HTTPS'
}

mySystem.api -[calls]-> internalBackend 'Routes uploads' {
  technology 'HTTP/8080'
}
```

Use `calls`, `reads`, `writes`, or `async` in the arrow. Put `Manual`, `HTTPS`, and `HTTP/8080` in the `technology` field on the system-model relationship. `HTTPS` is a technology value, not a relationship kind, so `-[https]->` is the wrong form. Keep deployment relationships only for rare infrastructure-specific facts that are not already expressed by the logical model.