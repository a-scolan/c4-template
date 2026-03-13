Put it in the template project: logical elements in `projects/template/system-model.c4`, views in `projects/template/system-views.c4`. That matches the workspace layout, and `projects/template/likec4.config.json` already includes `../shared`.

Model skeleton:
model {
  user = Actor_Person 'User'

  mySystem = System_Existing 'My System' {
    webapp = Container_Webapp 'Web Application'
    api = Container_Api 'API Server'
    database = Container_Database 'Database'
  }

  emailService = System_External 'Email Service'

  user -[calls]-> mySystem.webapp 'Interacts with' { technology 'Manual' }
  mySystem.webapp -[calls]-> mySystem.api 'Makes API requests' { technology 'HTTPS' }
  mySystem.api -[reads]-> mySystem.database 'Queries data' { technology 'PostgreSQL' }
  mySystem.api -[writes]-> mySystem.database 'Persists data' { technology 'PostgreSQL' }
  mySystem.api -[calls]-> emailService 'Sends notifications' { technology 'HTTPS' }
}

View skeleton:
views 'C2' {
  view c2_containers {
    title 'Containers'
    include user
    include mySystem.*
    include mySystem.webapp with { navigateTo c2_webapp_details }
    include emailService

    rank source { user }
    rank sink { mySystem.database, emailService }
  }

  view c2_webapp_details {
    title 'Web App Detail'
    include user
    include mySystem.webapp
    include mySystem.api

    rank source { user }
    rank sink { mySystem.api }
  }
}

If you also want the top-level click-through, keep `mySystem with { navigateTo c2_containers }` in the C1 view.
