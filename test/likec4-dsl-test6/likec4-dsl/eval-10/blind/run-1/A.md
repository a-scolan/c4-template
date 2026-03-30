```likec4
specification {
  element service
  relationship reads
  deploymentNode node
}

model {
  frontend = service 'Frontend' #next
  db = service 'DB'

  frontend -> db [reads]
}

deployment {
  prod = node 'prod' {
    eu = node 'eu' {
      web = node 'web' {
        frontend = frontend #gamma
        db = db
      }
    }
  }
}

views {
  deployment view rel_only_next of prod.eu.web {
    include * -> * where source.tag is #next
  }

  deployment view rel_only_gamma of prod.eu.web {
    include * -> * where source.tag is #gamma
  }

  deployment view rel_only_missing of prod.eu.web {
    include * -> * where source.tag is #missing
  }
}
```