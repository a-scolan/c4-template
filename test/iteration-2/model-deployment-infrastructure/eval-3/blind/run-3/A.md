Short answer: **not for normal app traffic**.

`Prod.Web.webApp -[https]-> Prod.App.apiApp` and `Prod.App.apiApp -[tcp]-> Prod.Data.dbApp` should usually **not** be manually added in `deployment.c4` when those interactions already exist in the logical model.

Correct pattern:

- Put relationship semantics and technology (`HTTPS`, `TCP/27017`, etc.) on logical model relationships.
- Use `instanceOf` in deployment nodes.
- Let LikeC4 inherit and render runtime relationships automatically.

Only add deployment-specific edges for operational/infrastructure flows not represented logically (monitoring scrape, backup replication, bastion SSH, log shipping).