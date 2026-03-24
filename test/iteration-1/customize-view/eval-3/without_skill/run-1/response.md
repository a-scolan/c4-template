view c2_containers of mySystem {
  link "Internal spec" "https://internal.example/specs/containers"

  style * {
    opacity 40
  }

  style mySystem.api {
    color primary
    opacity 100
  }

  mySystem.webapp {
    navigateTo c2_webapp_details
  }
}

This stays at view-level customization only: emphasis, layout, drill-down, and links. It stops before adding or renaming elements, changing relationships, or restructuring the underlying model.
