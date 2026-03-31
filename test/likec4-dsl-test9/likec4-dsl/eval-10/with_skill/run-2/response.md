```likec4
specification {
  element system
  element webapp
  element database
  relationship reads
  deploymentNode env
  deploymentNode region
  deploymentNode node
  tag next
  tag gamma
  tag missing
}

model {
  sys = system "sys" {
    frontend = webapp "frontend" {
      #next
    }
    db = database "db"

    frontend -[reads]-> db
  }
}

deployment {
  env prod {
    region eu {
      node web {
        frontend = instanceOf sys.frontend {
          #gamma
        }
      }
      node data {
        db = instanceOf sys.db
      }
    }
  }
}

views {
  deployment view rel_only_next {
    include * -> * where source.tag is #next
  }

  deployment view rel_only_gamma {
    include * -> * where source.tag is #gamma
  }

  deployment view rel_only_missing {
    include * -> * where source.tag is #missing
  }
}
```