views 'C2' {
  view containers_overview {
    include *
    include user with { rank source }
  }
}

This keeps the customization minimal: one obvious anchor, no pile of `rank` directives, and no unnecessary structural changes.
