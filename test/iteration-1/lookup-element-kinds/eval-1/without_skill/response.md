These are two different taxonomies.

In deployment, use the relationship kinds declared in `projects/shared/spec-deployment.c4`.

- Use `tcp` when you want to show network connectivity between an app VM and a database VM.
- Use `sql` when you want to show the database protocol / database access link more specifically.
- Do not use `calls` there as the deployment relationship vocabulary.

In the logical application model, use the relationship kinds declared in `projects/shared/spec-global.c4`.

- `calls` is valid for service-to-service or user-to-application interactions.
- `reads` and `writes` are the right logical kinds for application-to-database interactions.

So:

- deployment side: `tcp` or `sql` depending on the level of detail you want
- logical model side: `calls`, `reads`, `writes` as appropriate

You can confirm this split in `projects/shared/spec-deployment.c4`, `projects/shared/spec-global.c4`, and the logical examples in `projects/template/system-model.c4` or `projects/spec-showcase/containers.c4`.