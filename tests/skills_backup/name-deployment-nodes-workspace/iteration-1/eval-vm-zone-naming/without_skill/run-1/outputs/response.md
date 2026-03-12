Je proposerais quelque chose comme ça :

- environnement : `Production`
- zones : `AppServers`, `Workers`, `DataServers`, `MonitoringTier`
- VM : `ProdApiVM`, `prod_upload_vm`, `WorkerServer1`, `MongoServer`

Le principal est que l'équipe comprenne à quoi correspond chaque machine, donc des noms assez parlants suffisent.