# Deployment-Instance Tag Cumulativity Fixture

Paste this as a single `.c4` file. The three deployment views prove that `prod.eu.web.frontend` carries **both** `#next` (inherited from the logical model element `frontend`) and `#gamma` (added directly on the deployment instance), while `#missing` matches nothing.

```likec4
specification {
  element system
  element database
  deploymentNode environment
  deploymentNode zone
  deploymentNode vm
  tag next
  tag gamma
  tag missing
}

model {
  frontend = system "Frontend" {
    #next
  }

  db = database "DB"

  frontend -> db "reads"
}

deployment {
  prod = environment "Prod" {
    eu = zone "EU" {
      web = vm "Web VM" {
        frontend = instanceOf frontend {
          #gamma
        }
      }
      data = vm "Data VM" {
        db = instanceOf db
      }
    }
  }
}

views {
  // Renders: prod.eu.web.frontend -> prod.eu.data.db
  // Because #next is inherited from the logical model element
  deployment view rel_only_next {
    include * -> * where source.tag is #next
  }

  // Renders: prod.eu.web.frontend -> prod.eu.data.db
  // Because #gamma was added directly on the deployment instance
  deployment view rel_only_gamma {
    include * -> * where source.tag is #gamma
  }

  // Renders: nothing (empty view)
  // No element in the deployment carries #missing
  deployment view rel_only_missing {
    include * -> * where source.tag is #missing
  }
}
```

## Why the first two views render the relation and the third is empty

Deployment-instance tags are **cumulative**:

- The deployment instance `prod.eu.web.frontend` is declared as `instanceOf frontend`.
- It automatically inherits all tags from the logical element `frontend` — in this case `#next`.
- The `#gamma` tag added in the deployment block is merged on top; it does not replace the inherited tags.
- The effective tag set of `prod.eu.web.frontend` is therefore `{ #next, #gamma }`.

The `where source.tag is #next` predicate matches because `#next` is in that cumulative set.
The `where source.tag is #gamma` predicate matches because `#gamma` is also in that set.
The `where source.tag is #missing` predicate matches nothing, producing an empty view.
