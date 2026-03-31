```c4
specification {
  element service

  deploymentNode env
  deploymentNode region
  deploymentNode node
}

model {
  service frontend #next
  service db

  frontend -> db "reads"
}

deployment {
  env prod {
    region eu {
      node web {
        instance frontend #gamma
      }

      node data {
        instance db
      }
    }
  }
}

views {
  deployment view rel_only_next {
    include * -> * where source.tag is #next
  }

  deployment view rel_only_gamma {
    include * -> * where source.tag is #gamma
  }

  deployment view rel_only_missing {
    include * -> * where source.tag is #missing
  }
}
```

Expected behavior:
- `rel_only_next` renders the `reads` relationship because `prod.eu.web.frontend` cumulatively has logical tag `#next`.
- `rel_only_gamma` renders the same `reads` relationship because the deployment instance adds `#gamma`.
- `rel_only_missing` renders empty.