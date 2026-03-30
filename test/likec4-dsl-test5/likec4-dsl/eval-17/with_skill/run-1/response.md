This happens because references are resolved by lexical scope in each file; across files, non-global local paths like `backend.api` are not guaranteed to resolve, so you must use the fully qualified name (FQN).

Correct cross-file relationship:

```likec4
model {
  cloud.backend.api -> cloud.db
}
```
