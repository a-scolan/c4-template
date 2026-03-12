```likec4
view existing_c2_view {
  style * {
    color muted
    opacity 35%
  }

  style element.tag = #api {
    color primary
    opacity 100%
  }

  include webApp with {
    navigateTo existing_webapp_detail_view
  }

  link https://docs.internal/spec 'Internal specification'
}
```

This skill stops at view customization: styling, light layout hints, `navigateTo`, and external `link` entries.
If you need to change included elements, parent context, or create a new C3/detail view, hand that off to `design-view`. 