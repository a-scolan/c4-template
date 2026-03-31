```likec4
specification {
  element webapp
  element database

  deploymentNode env
  deploymentNode region
  deploymentNode node

  tag next
  tag gamma
  tag missing
}

model {
  frontend = webapp "Frontend" {
    #next
  }

  db = database "DB"

  frontend -> db "reads"
}

deployment {
  env prod {
    region eu {
      node web {
        frontend = instanceOf frontend {
          #gamma
        }
      }

      node data {
        db = instanceOf db
      }
    }
  }
}

views {
  deployment view rel_only_next {
    include prod.eu.web.frontend -> prod.eu.data.db where source.tag is #next
  }

  deployment view rel_only_gamma {
    include prod.eu.web.frontend -> prod.eu.data.db where source.tag is #gamma
  }

  deployment view rel_only_missing {
    include prod.eu.web.frontend -> prod.eu.data.db where source.tag is #missing
  }
}
```