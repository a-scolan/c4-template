```likec4
view c2_containers {
  link https://intranet.example.com/specs/web-platform 'Internal spec docs'

  style * {
    color muted
  }

  style element.tag == #Api {
    color primary
  }

  include mySystem.webapp with {
    navigateTo c2_webapp_details
  }
}
```

This stays within view customization. If you need a new structural or C3 view, treat that as a separate design step.