This fails because cross-file references do not automatically resolve through local lexical scope: in another file, `backend.api` is not visible as a local symbol, so you must reference the element by its full FQN.

Use the relationship with FQNs:

```likec4
cloud.backend.api -> cloud.db
```