views 'C2' {
  view containers_overview {
    include *

    style * { color muted; opacity 20% }
    style api.*, gateway.* { color primary; opacity 100% }
  }
}
