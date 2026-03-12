Those relationships generally should **not** be added in `deployment.c4` for normal application traffic.

If `Prod.Web.webApp` is an instance of the logical web container, `Prod.App.apiApp` is an instance of the logical API container, and `Prod.Data.dbApp` is an instance of the logical database container, then the normal communication paths should be modeled on the **system-model relationships** and inherited into deployment through `instanceOf`.

So the protocol and port details should usually live on the logical relationships, for example:

```likec4
web -> api {
  calls 'Uses API'
  technology 'HTTPS'
}

api -> db {
  reads 'Reads documents'
  technology 'TCP/27017'
}
```

Or, if a non-default application port matters:

```likec4
web -> api {
  calls 'Uses API'
  technology 'HTTP/8080'
}
```

That is the preferred place for application protocol details, because:

- it keeps behavior attached to the logical architecture
- deployment instances inherit those relationships through `instanceOf`
- it avoids duplicating the same app traffic in every deployment environment

So for your case, the default answer is:

- **do not add** `Prod.Web.webApp -[https]-> Prod.App.apiApp` just to restate normal web-to-API traffic
- **do not add** `Prod.App.apiApp -[tcp]-> Prod.Data.dbApp` just to restate normal API-to-database traffic

Add deployment relationships only when they represent infrastructure-specific exceptions rather than ordinary inherited application communication. Good examples are:

- monitoring or log shipping
- replication or backup transfer
- bastion/admin access
- load balancer to target-group wiring
- explicit firewall / router / network-hop documentation
- other deployment-only infrastructure flows

So the rule is: **business/application communication goes in the system model; deployment edges are for infrastructure-specific cases.** Nice and boring—which, in deployment modeling, is usually a compliment.