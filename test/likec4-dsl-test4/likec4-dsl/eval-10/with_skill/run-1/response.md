## Deployment-Instance Tag Accumulation Fixture

Below is one paste-ready `.c4` file that proves deployment-instance tags are cumulative for `source.tag` filtering.

**Tag accumulation rule:** A deployment instance inherits all tags from its logical element **and** adds any tags declared on the instance itself. Both sets are active simultaneously for `where source.tag is` filters.

```likec4
specification {
  element webapp
  element database
  tag next
  tag gamma
  tag missing
  deploymentNode environment
  deploymentNode vm
}

model {
  frontend = webapp "Frontend" {
    #next
  }
  db = database "DB"
  frontend -> db "reads"
}

deployment {
  prod = environment {
    eu = environment {
      web = vm {
        // This instance has FQN: prod.eu.web.frontend
        // Tags: #next (inherited from logical frontend) + #gamma (added here) = cumulative
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
  // Renders: #next comes from the logical model's `frontend` element.
  // Instance inherits it, so the reads relation appears.
  deployment view rel_only_next {
    include * -> * where source.tag is #next
  }

  // Renders: #gamma is added by deployment instance prod.eu.web.frontend.
  // Because tags are cumulative, this filter also matches and the reads relation appears.
  deployment view rel_only_gamma {
    include * -> * where source.tag is #gamma
  }

  // Empty: no logical element or deployment instance has #missing.
  // Filter matches nothing → view renders empty.
  deployment view rel_only_missing {
    include * -> * where source.tag is #missing
  }
}
```

### What each view proves

| View | Filter | Result | Reason |
|---|---|---|---|
| `rel_only_next` | `source.tag is #next` | **renders** `reads` | `#next` is on the logical `frontend`; inherited by the instance |
| `rel_only_gamma` | `source.tag is #gamma` | **renders** `reads` | `#gamma` is added by `prod.eu.web.frontend`; cumulative with logical tags |
| `rel_only_missing` | `source.tag is #missing` | **empty** | No element (logical or instance) carries `#missing` |

The pair `rel_only_next` + `rel_only_gamma` together prove accumulation: the same deployment instance satisfies **both** filters simultaneously, one inherited from the logical element and one added at the deployment level.
