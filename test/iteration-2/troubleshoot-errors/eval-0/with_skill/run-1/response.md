1. **Probable error category**
   - Mixed taxonomy + FQN resolution issue (`Unknown kind` + `Element not found`).

2. **Root cause**
   - `Container_WebUi` is not a declared kind in shared specs (likely wrong casing/spelling).
   - `api` is referenced as a short name where a full FQN is required.

3. **Verification step**
   - Compare element kinds against `projects/shared/spec-*.c4` and confirm exact spelling.
   - Locate the real API element id in the model hierarchy, then confirm its full FQN (for example `corePlatform.api`).

4. **Minimal fix**

```likec4
model {
  corePlatform = system 'Core Platform' {
    api = Container_Api 'API'
    webUi = Container_WebUI 'Web UI'
  }

  // Use FQN, not short name
  corePlatform.webUi -[calls]-> corePlatform.api 'Calls API'
}
```