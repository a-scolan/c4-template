```likec4
specification {
  element service
  element database

  deploymentNode environment
  deploymentNode region
  deploymentNode node
}

model {
  frontend = service 'Frontend' #next
  db = database 'DB'

  frontend -> db 'reads'
}

deployment {
  prod = environment 'prod' {
    eu = region 'eu' {
      web = node 'web' {
        frontend = frontend #gamma
      }
      data = node 'data' {
        db = db
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

`rel_only_next` and `rel_only_gamma` both include the deployed `frontend -> db` `reads` relationship, proving the source instance carries both the logical tag `#next` and the instance tag `#gamma`. `rel_only_missing` stays empty.