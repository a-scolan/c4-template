```likec4
specification {
  element service
  element database
  tag next
  tag gamma
  tag missing
  deploymentNode env
  deploymentNode region
  deploymentNode node
}

model {
  frontend = service {
    #next
    -> db 'reads'
  }
  db = database
}

deployment {
  prod = env {
    eu = region {
      web = node {
        frontend = instanceOf frontend {
          #gamma
        }
      }
      data = node {
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
```