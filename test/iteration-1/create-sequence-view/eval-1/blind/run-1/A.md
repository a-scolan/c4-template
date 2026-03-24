Do not write `api_container -> api_container.auth_component` as a sequence step. That mixes containment with runtime interaction. In a dynamic view, participants should be at one abstraction level. Correct options:
- Container-level story: keep `webApp -> api_container "Authenticate user"` and hide the internal component.
- Component-level story: use the component directly as the participant.
Example:
```likec4
dynamic view auth_flow {
  webApp -> api_container.auth_component "Submit credentials"
  api_container.auth_component -> primaryDatabase "Load account and verify password"
  api_container.auth_component -> webApp "Return token/session"
}
```
Rule of thumb: avoid parent -> child hops inside the same dynamic sequence.
