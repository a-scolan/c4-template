`ops.c4` is validated in the same global model as `base.c4`, but name resolution is still scope-based.

Why `backend.api -> cloud.db` fails:

1. `backend.api` is **not** a valid top-level reference.  
   In `base.c4`, `api` is nested under `cloud.backend`, so its FQN is `cloud.backend.api`.  
   From another file at top level, `backend.api` cannot be resolved because there is no root element named `backend`.

2. `cloud.db` must exist as that exact FQN.  
   With your shown definition (`cloud = system { backend = container { api = service } }`), no `db` is declared, so `cloud.db` is also unresolved unless defined elsewhere.

Correct cross-file relationship (using FQNs):

`cloud.backend.api -> cloud.db`

(And if `cloud.db` is not defined yet, define it first, then keep the relationship above.)