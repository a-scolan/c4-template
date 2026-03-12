A dynamic view should not show `parent -> own-child` such as `api_container -> api_container.auth_component`, because that hides the real initiator of the interaction. Instead, target the concrete component directly from the actor that starts the scenario.

In `projects/spec-showcase/component-views.c4`, add a separate use-case view like this:

```likec4
views 'Use Cases' {
  dynamic view authentication_journey of api_container {
    title 'Authentication Journey'

    include person_external
    include api_container.auth_component
    include api_container.routing_component
    include component_database

    person_external -> api_container.auth_component 'Submits credentials'
    api_container.auth_component -> component_database 'Loads user record'
    api_container.auth_component -> api_container.routing_component 'Passes authenticated request'
    api_container.routing_component -> person_external 'Returns authentication result'
  }
}
```

That keeps the actor targeting `api_container.auth_component` directly and uses only plain `->` arrows with action labels.
