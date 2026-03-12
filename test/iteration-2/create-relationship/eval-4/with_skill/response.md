No — do not keep normal browser/application traffic duplicated in deployment just to show it on the diagram.

That relationship should live in the **system model**, and deployment instances should inherit it through `instanceOf`. Reserve deployment relationships for rare infrastructure-only facts such as replication, monitoring scrapes, or bastion access.

Use the technology values on the logical model relationships, like this:

```likec4
user -[calls]-> webApp 'Uses UI' {
  technology 'Manual'
}

webApp -[calls]-> apiApp 'Sends request' {
  technology 'HTTPS'
}

apiApp -[calls]-> internalService 'Routes request' {
  technology 'HTTP/8080'
}
```

Guidance:
- Use `technology 'Manual'` for human interaction.
- Use `technology 'HTTPS'` for browser or service traffic.
- Use `technology 'HTTP/8080'` only when the non-default internal port matters.

So `Prod.Web.webApp -[https]-> Prod.App.apiApp` is an anti-pattern for normal app traffic; model it once in `model {}` and let deployment inherit it.
