That is not the right default place for those relationships. `Prod.Web.webApp -[https]-> Prod.App.apiApp` and `Prod.App.apiApp -[tcp]-> Prod.Data.dbApp` should usually not be added manually in `deployment.c4` just to show protocols or ports.

The skill’s rule is: put normal application traffic on the logical model relationships and put the technology there as well, for example `HTTPS`, `HTTP/8080`, `MongoDB`, or `TCP/27017`. Then let the deployment instances inherit those relationships automatically through `instanceOf`.

Only add deployment relationships when they are infrastructure-specific and not already part of the logical model, such as monitoring scrapes, backup traffic, bastion access, log shipping, or replication. If you really need one of those infra-only deployment links, then using deployment relationship kinds like `https` or `tcp` is fine, but use them sparingly.
