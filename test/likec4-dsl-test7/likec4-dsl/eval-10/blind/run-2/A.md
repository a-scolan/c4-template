```c4
specification {
  element person
  element system
  deploymentNode environment

  relationship reads
}

model {
  user = person "User"
  frontend = system "Frontend" #next
  db = system "Database"

  user -> frontend "uses"
  frontend -> db reads "reads"
}

deployment {
  prod = environment "prod" {
    eu = environment "eu" {
      web = environment "web" {
        frontend = frontend "frontend" #gamma
      }
      db = db "db"
    }
  }
}

deployment view rel_only_next of prod {
  include *
  include "* -> *" where source.tag is #next
  autoLayout lr
}

deployment view rel_only_gamma of prod {
  include *
  include "* -> *" where source.tag is #gamma
  autoLayout lr
}

deployment view rel_only_missing of prod {
  include *
  include "* -> *" where source.tag is #missing
  autoLayout lr
}
```