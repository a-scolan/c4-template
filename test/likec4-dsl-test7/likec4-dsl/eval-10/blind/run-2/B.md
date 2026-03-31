```likec4
specification {
  element service
  element database
  relationship reads

  deploymentNode environment
  deploymentNode zone
  deploymentNode node

  tag next
  tag gamma
  tag missing
}

model {
  frontend = service {
    #next
    -[reads]-> db
  }

  db = database
}

deployment {
  prod = environment {
    eu = zone {
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