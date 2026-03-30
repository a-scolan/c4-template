# Deployment-Instance Tag Cumulative Fixture

Paste-ready `.c4` file demonstrating that deployment-instance tags are **cumulative**: the deployed instance `prod.eu.web.frontend` inherits `#next` from its logical element `frontend` **and** carries the instance-level `#gamma`. A `where source.tag is` filter matches either tag independently.

```c4
// Minimal fixture: proves deployment-instance tags are cumulative for source.tag filtering.
// Logical `frontend` carries #next; its deployment instance adds #gamma.
// Both tags coexist on the deployed instance, so:
//   rel_only_next    → renders the `reads` relation  (cumulative: logical tag inherited)
//   rel_only_gamma   → renders the `reads` relation  (instance-level tag matched)
//   rel_only_missing → renders empty                 (#missing appears on neither)

specification {
  element system
  element database
  relationship reads
  tag next
  tag gamma
  tag missing
}

model {
  frontend = system 'Frontend' {
    #next
  }

  db = database 'Database'

  frontend -> db 'reads' {
    kind reads
  }
}

deployment {
  node prod {
    node eu {
      node web {
        // Inherits #next from logical frontend; #gamma added at instance level.
        instance frontend = frontend {
          #gamma
        }
      }
    }
    node data {
      instance db = db
    }
  }
}

// Matches: prod.eu.web.frontend has #next (inherited from logical element)
deployment view rel_only_next {
  title 'Reads — source tagged #next (inherited)'
  include -> where source.tag is #next
}

// Matches: prod.eu.web.frontend has #gamma (added at deployment instance level)
deployment view rel_only_gamma {
  title 'Reads — source tagged #gamma (instance)'
  include -> where source.tag is #gamma
}

// No match: neither the logical element nor the instance declares #missing → empty view
deployment view rel_only_missing {
  title 'Reads — source tagged #missing (empty)'
  include -> where source.tag is #missing
}
```
```c4
specification {
  element person
  element system
  relationship reads
  tag next
  tag gamma
}

model {
  user = person 'User'
  app = system 'App' {
    frontend = system 'Frontend' #next
    db = system 'DB'
  }

  user -> app.frontend 'uses'
  app.frontend -> app.db reads
}

deployment {
  environment prod {
    eu = deploymentNode 'eu' {
      web = deploymentNode 'web' {
        frontend = app.frontend #gamma
      }
      db = app.db
    }
  }
}

views {
  deployment prod.eu.web rel_only_next {
    include *
    include -> where source.tag is #next
    autolayout lr
  }

  deployment prod.eu.web rel_only_gamma {
    include *
    include -> where source.tag is #gamma
    autolayout lr
  }

  deployment prod.eu.web rel_only_missing {
    include *
    include -> where source.tag is #missing
    autolayout lr
  }
}
```
## Why this proves cumulative tags

| View | Filter | Tag origin | Result |
|---|---|---|---|
| `rel_only_next` | `source.tag is #next` | Logical `frontend` | Renders `reads` relation |
| `rel_only_gamma` | `source.tag is #gamma` | Deployment instance | Renders `reads` relation |
| `rel_only_missing` | `source.tag is #missing` | Not declared anywhere | Empty view |

`prod.eu.web.frontend` effectively has the union `{#next, #gamma}` — tags are **not replaced** at the instance level, they accumulate. `rel_only_next` and `rel_only_gamma` both include the same relationship, confirming this behaviour.
