`api_container -> api_container.auth_component` is the wrong abstraction for a dynamic view. It shows a container calling one of its own children, while the repo's C3 style models runtime behavior between peer participants.

Use one of these instead:
- Keep it at container level: `webApp -> api_container 'Authenticate user'`.
- If you want internal detail, make it a component-level dynamic view and show peer steps, for example:
  `webApp -> api_container.routing_component 'POST /login'`
  `api_container.routing_component -> api_container.auth_component 'Validate credentials/token'`

That matches the local component showcase, which models `routing_component -> auth_component` rather than `api_container -> auth_component`.
