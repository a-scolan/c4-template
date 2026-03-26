view c2 {
  style * {
    opacity 35%
  }

  style tag "api" {
    opacity 100%
  }

  link "Internal docs" "https://intranet.example/specs/c2"
  webapp -> webapp-detail
}

This skill stops at proposing the view customization block. It does not perform model refactoring, relationship redesign, or non-view architectural changes.