```likec4
specification {
  element app
  element db
  deploymentNode env
  deploymentNode region
  deploymentNode vm
  tag next
  tag gamma
  tag missing
}

model {
  frontend = app {
    #next
    -> db "reads"
  }
  db = db
}

deployment {
  prod = env {
    eu = region {
      web = vm {
        frontend = instanceOf frontend {
          #gamma
        }
      }
      data = vm {
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