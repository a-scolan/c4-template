```likec4
specification {
  element app
  deploymentNode node
}

model {
  frontend = app {
    #next
    -> db "reads"
  }
  db = app
}

deployment {
  prod = node {
    eu = node {
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