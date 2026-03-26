Deployment app VM ↔ database VM should use deployment relationship taxonomy:

- `sql` for database protocol interactions
- `tcp` for generic network transport
- not `calls`

In the logical application model, valid relationship kinds are:

- `calls`, `async`, `reads`, `writes`, `uses`

Therefore:

- `calls` is logical-model valid
- `tcp/sql` are deployment valid