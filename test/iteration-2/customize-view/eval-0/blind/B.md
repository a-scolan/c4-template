```likec4
view existing_c2_view {
  autoLayout LeftRight

  include user with {
    rank source
  }

  include webApp with {
    navigateTo existing_webapp_detail_view
  }
}
```