That is **usually not the right place** for those relationships.

For normal application traffic such as:

- `webApp -> apiApp`
- `apiApp -> dbApp`

avoid manually adding deployment edges just to show protocols or ports. Those details should live on the **system-model relationships**, for example:

```likec4
web -[calls]-> api 'User requests' {
  technology 'HTTPS'
}

api -[reads-writes]-> db 'Store documents' {
  technology 'TCP/27017'
}
```

Then, in `deployment.c4`, your deployed instances use `instanceOf`:

```likec4
webApp = Node_App "Web" {
  instanceOf docPlatform.web
}

apiApp = Node_App "API" {
  instanceOf docPlatform.api
}

dbApp = Node_App "MongoDB" {
  instanceOf docPlatform.mongoDb
}
```

Because of `instanceOf`, the deployment instances inherit the logical relationships automatically. That is the normal path.

So for your examples:

- `Prod.Web.webApp -[https]-> Prod.App.apiApp`
- `Prod.App.apiApp -[tcp]-> Prod.Data.dbApp`

**do not add them** if they are just the deployed form of ordinary application traffic already described in the logical model.

Add deployment relationships only when they are **infrastructure-specific** and not already represented logically, such as:

- monitoring or log shipping
- backup or replication links
- bastion/admin access
- operational agents
- an explicit network hop that matters operationally

Short version: **protocols and ports belong on system-model relationships; deployment instances inherit them through `instanceOf`; deployment edges are for infra exceptions, not routine app traffic.**