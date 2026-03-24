Do not use `api_container -> api_container.auth_component` in a dynamic view. That is a parent -> own-child interaction, which is the main anti-pattern here.

Use the real caller to target the child directly, or stay at container level if component detail is not needed:

views 'Use Cases' {
  dynamic view authenticationFlow {
    title 'Authentication Flow'
    user -> webApp 'Starts login'
    webApp -> api_container.auth_component 'POST /login'
    api_container.auth_component -> primaryDatabase 'Reads user'
  }
}

If you do not need component-level detail, simplify it further to `webApp -> api_container 'POST /login'`.
