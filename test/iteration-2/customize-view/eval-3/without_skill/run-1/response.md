view c2_containers {
  include *

  style element.tag == #Api {
    opacity 100%
    border solid
  }

  style element.tag != #Api {
    opacity 20%
  }

  webapp {
    navigateTo c3_webapp
    link 'Internal docs' 'https://intranet.example.local/architecture/specs'
  }
}

This skill stops at view-level customization (layout, filtering, highlighting, links, navigation). It does not create or change the underlying model elements/relationships.
