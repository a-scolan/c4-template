view containers_overview {
  autoLayout

  include user with { rank source }
}

I would stop there unless the preview is still unclear; I would avoid piling on rank same, rank source, and rank sink directives because that is what makes the layout brittle.
