specification {
  element service
  deploymentNode env
  deploymentNode region
  deploymentNode vm

  tag next
  tag gamma
  tag missing
}

model {
  frontend = service {
    #next
  }
  db = service

  frontend -> db 'reads'
}

deployment {
  prod = env {
    eu = region {
      web = vm {
        frontend = instanceOf frontend {
          #gamma
        }
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
