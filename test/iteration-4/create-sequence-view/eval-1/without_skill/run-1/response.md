Do not use `api_container -> api_container.auth_component` as if the container itself were an active caller. Either stay at container level with `webApp -> api_container 'Authenticate user'`, or switch to a component-focused dynamic view and target the component directly:
views {
  dynamic view auth_flow {
    title 'Authentication inside API'
    include webApp, api_container.auth_component, api_container.session_component

    webApp -> api_container.auth_component 'Submit credentials'
    api_container.auth_component -> api_container.session_component 'Create session'
  }
}
In short: use the parent container for container-level steps, use child components for component-level steps, and avoid parent-container-to-own-component as the narrative interaction.
