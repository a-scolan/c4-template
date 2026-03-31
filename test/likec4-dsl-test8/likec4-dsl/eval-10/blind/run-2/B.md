specification {
  element app
  element database

  deploymentNode env
  deploymentNode region
  deploymentNode vm

  tag next
  tag gamma
  tag missing
}

model {
  app frontend {
    #next
  }

  database db

  frontend -> db "reads"
}

deployment {
  env prod {
    region eu {
      vm web {
        frontend = instanceOf frontend {
          #gamma
        }
      }
      vm data {
        db = instanceOf db
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
