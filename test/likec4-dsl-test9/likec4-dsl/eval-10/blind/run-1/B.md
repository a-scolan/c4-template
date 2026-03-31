Paste this into a single `.c4` file:

```c4
specification {
  element service
  element database

  deploymentNode environment
  deploymentNode region
  deploymentNode node
}

model {
  frontend = service 'frontend' {
    tags #next
  }

  db = database 'db'

  frontend -> db 'reads'
}

deployment {
  prod = environment 'prod' {
    eu = region 'eu' {
      web = node 'web' {
        frontend = instanceOf frontend {
          tags #gamma
        }
      }

      data = node 'data' {
        db = instanceOf db
      }
    }
  }
}

views {
  deployment view rel_only_next of prod {
    include relationships where source.tag is #next
  }

  deployment view rel_only_gamma of prod {
    include relationships where source.tag is #gamma
  }

  deployment view rel_only_missing of prod {
    include relationships where source.tag is #missing
  }
}
```

Expected behavior:

- `rel_only_next` renders the `reads` relationship because the source instance inherits `#next` from logical `frontend`.
- `rel_only_gamma` also renders the same `reads` relationship because the deployment instance adds `#gamma`.
- `rel_only_missing` renders empty because the source has no `#missing` tag.
