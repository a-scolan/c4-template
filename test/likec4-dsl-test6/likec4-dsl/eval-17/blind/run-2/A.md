`backend.api -> cloud.db` fails because name resolution is lexical: in `ops.c4` there is no top-level symbol named `backend`, since `backend` is nested inside `cloud` in `base.c4`. Files contribute to the same model, but they do not change the element hierarchy or make nested names addressable without their full path, so cross-file references to nested elements must use FQNs.

Corrected relationship:

```likec4
cloud.backend.api -> cloud.db
```