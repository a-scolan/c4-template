view c2_containers {
  style * {
    color muted
  }

  style * where kind is Container_Api
     or kind is Container_Api_Geo {
    color primary
  }

  include mySystem.webapp with {
    navigateTo c2_webapp_details
    link https://intranet.example.com/specs/webapp 'Internal spec docs'
  }
}

This stops at view-level styling, linking, and navigation. Creating a new structural variant or a new C3/detail view is a separate design change.