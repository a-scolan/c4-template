`backend.api -> cloud.db` fails in `ops.c4` because LikeC4 uses lexical scoping, and across files nested elements are not available by partial path; outside the `cloud` body you must reference nested elements by their full FQNs.

Correct cross-file relationship:

```likec4
model {
  cloud.backend.api -> cloud.db
}
```