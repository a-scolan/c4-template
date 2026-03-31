```c4
specification {
  element service
  element database
  deploymentNode node
}

model {
  frontend = service 'frontend' {
    #next
  }

  db = database 'db'

  frontend -> db 'reads'
}

deployment {
  prod = node 'prod' {
    eu = node 'eu' {
      web = node 'web' {
        frontend = frontend {
          #gamma
        }
      }

      db = db
    }
  }
}

deployment view rel_only_next of prod {
  include * -> * where source.tag is #next
}

deployment view rel_only_gamma of prod {
  include * -> * where source.tag is #gamma
}

deployment view rel_only_missing of prod {
  include * -> * where source.tag is #missing
}
```