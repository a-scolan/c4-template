# LikeC4 Deployment-Instance Tag Accumulation Fixture

Below is a single paste-ready `.c4` file. The key claim it proves: a deployment instance's effective tag set is the **union** of the logical element's tags and any tags added directly on the instance. Filtering `where source.tag is #next` hits the instance because `frontend` carries `#next`; filtering `where source.tag is #gamma` also hits it because the instance itself adds `#gamma`; filtering by `#missing` finds nothing.

```c4
specification {
  element system
  element database

  deployment {
    env
    zone
    node
  }

  tag next
  tag gamma
  tag missing
}

model {
  frontend = system 'Frontend' {
    #next
    -> db 'reads'
  }

  db = database 'Database'
}

deployment {
  prod = env 'Production' {
    eu = zone 'EU' {
      web = node 'Web Node' {
        // Instance FQN becomes prod.eu.web.frontend
        // Effective tags: #next (inherited) + #gamma (added here)
        frontend = instanceOf frontend {
          #gamma
        }

        db = instanceOf db
      }
    }
  }
}

// Renders the 'reads' relation: source (prod.eu.web.frontend) has tag #next
deployment view rel_only_next {
  include * -> * where source.tag is #next
}

// Renders the 'reads' relation: source (prod.eu.web.frontend) has tag #gamma
deployment view rel_only_gamma {
  include * -> * where source.tag is #gamma
}

// Renders EMPTY: no deployed instance has tag #missing
deployment view rel_only_missing {
  include * -> * where source.tag is #missing
}
```

## How it works

| View | Filter tag | Instance effective tags | Match? | Result |
|---|---|---|---|---|
| `rel_only_next` | `#next` | `{#next, #gamma}` | Yes | `reads` edge rendered |
| `rel_only_gamma` | `#gamma` | `{#next, #gamma}` | Yes | `reads` edge rendered |
| `rel_only_missing` | `#missing` | `{#next, #gamma}` | No | Empty view |

### Observations

- **`instanceOf`** binds the deployment node to its logical element; LikeC4 merges the logical element's tags into the instance at view-resolution time.
- Tags declared inside the `instanceOf { … }` block are **additive** — they extend, not replace, the logical element's tag set.
- The `where source.tag is #tag` predicate on a wildcard relationship include (`* -> *`) is the most direct way to assert tag-based filtering without enumerating specific element paths.
- Removing the `#gamma` line from the `frontend` instance block would cause `rel_only_gamma` to also render empty, confirming the tag came from the instance, not the logical element.
