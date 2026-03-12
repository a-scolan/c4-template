No—creating `Container_UploadOrchestrator` just for one service is not a good fit here.

In this repo, kinds are shared, reusable building blocks defined in the shared specifications. Before adding any new kind, first check whether an existing one already covers the need. For an upload service, `Container_Api` is the obvious fit.

Only introduce a new kind if you have a reusable pattern that cannot be expressed with the existing shared kinds, and get approval before adding it to the shared specs.