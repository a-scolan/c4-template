# Deployment-instance cumulative tags fixture

```c4
specification {
  element app
  element database

  deploymentNode region
  deploymentNode host

  tag next
  tag gamma
  tag missing

  relationship reads
}

model {
  frontend = app 'Frontend' {
    #next
  }

  db = database 'Database'

  frontend -[reads]-> db 'reads'
}

deployment {
  prod = region 'Production' {
    eu = region 'EU' {
      web = host 'Web Host' {
        // instance inherits #next from logical frontend AND adds #gamma
        frontendInst = instanceOf frontend 'Frontend Instance' {
          #gamma
        }
      }
    }

    dbInst = instanceOf db 'DB Instance'
  }
}

views {
  // source.tag = #next (inherited from logical element) → renders reads relation
  deployment view rel_only_next {
    include * -> * where source.tag is #next
  }

  // source.tag = #gamma (set on instance itself) → renders reads relation
  deployment view rel_only_gamma {
    include * -> * where source.tag is #gamma
  }

  // source.tag = #missing (no element has this tag) → empty view
  deployment view rel_only_missing {
    include * -> * where source.tag is #missing
  }
}
```

## Why this works

Tags on a deployed instance are **cumulative**: the instance `frontendInst` carries every tag declared on its logical source element (`frontend → #next`) **plus** any tag declared on the instance itself (`#gamma`).

| View | `where` filter | Instance tags matched | Result |
|------|---------------|----------------------|--------|
| `rel_only_next` | `source.tag is #next` | `#next` inherited from `frontend` | `reads` edge rendered |
| `rel_only_gamma` | `source.tag is #gamma` | `#gamma` declared on instance | `reads` edge rendered |
| `rel_only_missing` | `source.tag is #missing` | — | empty view |

The `include * -> * where source.tag is <tag>` predicate therefore acts on the **merged** tag set of the deployed instance, not just on the instance's own tags or just the logical element's tags.
