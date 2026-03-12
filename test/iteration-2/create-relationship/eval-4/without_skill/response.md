For normal browser-to-app or app-to-app traffic, **do not keep that relationship in deployment**.

`Prod.Web.webApp -[https]-> Prod.App.apiApp` is usually the wrong place for standard application traffic. Model it in the **system model**, and let deployment instances inherit it through `instanceOf`.

A good pattern is:

```likec4
user -[calls]-> webApp 'Uses web application' {
  technology 'Manual'
}

webApp -[calls]-> apiApp 'Calls API' {
  technology 'HTTPS'
}

internalService -[calls]-> legacyApi 'Calls legacy endpoint' {
  technology 'HTTP/8080'
}
```

Where these values live:
- `Manual` -> relationship `technology` for human interaction
- `HTTPS` -> relationship `technology` for normal browser/service traffic
- `HTTP/8080` -> relationship `technology` only when you need to show a **non-default port**

Deployment relationships should be rare and reserved for **infrastructure-specific exceptions** that are not already captured by the logical model. In the common case, deployment instances inherit the system-model relationships via `instanceOf`, which keeps the model clean and avoids duplication.