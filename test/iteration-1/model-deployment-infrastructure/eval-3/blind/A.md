No: those deployment relationships should usually **not** be added for normal application traffic.

If `webApp`, `apiApp`, and `dbApp` are deployment instances of logical containers, the correct place for protocols and ports is the **system model** relationship, not duplicated edges in `deployment.c4`.

For example, put the technical detail here:

```likec4
model {
  documentPlatform.webApp -[calls]-> documentPlatform.api "Uses API" {
    technology "HTTPS"
  }

  documentPlatform.api -[reads]-> documentPlatform.mongoDb "Reads documents" {
    technology "MongoDB/TCP 27017"
  }
}
```

Then connect the deployed instances with `instanceOf`:

```likec4
ProdWebVm = Node_Vm "prod-web-vm" {
  webApp = Node_App "Web App" {
    instanceOf documentPlatform.webApp
  }
}

ProdApiVm = Node_Vm "prod-api-vm" {
  apiApp = Node_App "API" {
    instanceOf documentPlatform.api
  }
}

ProdMongoVm = Node_Vm "prod-mongo-vm" {
  dbApp = Node_App "MongoDB" {
    instanceOf documentPlatform.mongoDb
  }
}
```

Once you do that, the deployment instances inherit the logical relationships automatically through `instanceOf`. That is why adding `Prod.Web.webApp -[https]-> Prod.App.apiApp` and `Prod.App.apiApp -[tcp]-> Prod.Data.dbApp` is usually redundant for normal application traffic.

Keep deployment relationships only for infrastructure-specific exceptions, such as:

- monitoring or log shipping
- backup and restore flows
- replication links
- bastion or admin access
- an explicit network hop that matters operationally but is not part of the logical application design

So: move `HTTPS`, `HTTP/8080`, database ports, and similar protocol details to the system-model relationships, let deployment instances inherit them, and keep deployment edges sparse and infrastructure-focused.
