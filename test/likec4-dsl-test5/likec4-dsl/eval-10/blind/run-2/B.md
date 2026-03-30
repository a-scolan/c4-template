```likec4
specification {
  element webapp
  element database
  tag next
  tag gamma
  tag missing

  deploymentNode env
  deploymentNode region
  deploymentNode vm
}

model {
  frontend = webapp {
    #next
  }
  db = database
  frontend -> db "reads"
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
        instanceOf db
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