Add the Prometheus scrape relationship, because that is an operational infrastructure concern and usually does not belong in the logical business/application model. Model it against the real scrape target: if Prometheus hits the app metrics endpoint, relate Prometheus to the relevant `Node_App`; if it hits a node exporter or VM-level exporter, relate Prometheus to that VM-side deployment node instead.

Avoid duplicating the browser -> API traffic and the API -> database traffic if those already exist in the logical model. Those flows should stay defined once in the system model and be inherited automatically through `instanceOf` in deployment views.

A simple rule: add deployment relationships for monitoring, backups, bastion/admin access, replication, and other ops-only links; do not re-add normal user or service traffic just to show protocols or ports a second time.
