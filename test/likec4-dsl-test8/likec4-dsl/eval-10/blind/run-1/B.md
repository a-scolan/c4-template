```c4
specification {
  element service
  element database
  relationship reads

  deploymentNode environment
  deploymentNode region
  deploymentNode tier
}

model {
  frontend = service 'frontend' {
    #next
  }

  db = database 'db'

  frontend -> db [reads]
}

deployment {
  prod = environment 'prod' {
    eu = region 'eu' {
      web = tier 'web' {
        frontend = instanceOf frontend {
          #gamma
        }
      }

      data = tier 'data' {
        db = instanceOf db
      }
    }
  }
}

views {
  deployment view rel_only_next of prod {
    include * -> * where source.tag is #next
  }

  deployment view rel_only_gamma of prod {
    include * -> * where source.tag is #gamma
  }

  deployment view rel_only_missing of prod {
    include * -> * where source.tag is #missing
  }
}
```