```c4
specification {
  element service
  relationship reads
}

model {
  frontend = service "Frontend" {
    #next
  }

  db = service "DB"

  frontend -> db reads
}

deployment {
  node prod {
    node eu {
      node web {
        frontend = instanceOf frontend {
          #gamma
        }
      }

      node data {
        db = instanceOf db
      }
    }
  }
}

deployment view rel_only_next of prod.eu {
  include * -> * where source.tag is #next
}

deployment view rel_only_gamma of prod.eu {
  include * -> * where source.tag is #gamma
}

deployment view rel_only_missing of prod.eu {
  include * -> * where source.tag is #missing
}
```