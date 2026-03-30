```likec4
specification {
  element service
  element database
  deploymentNode environment
  deploymentNode region
  deploymentNode node
  relationship reads
}

model {
  frontend = service 'Frontend' #next
  db = database 'DB'

  frontend -> db reads
}

deployment {
  prod = environment 'prod' {
    eu = region 'eu' {
      web = node 'web' {
        frontend = frontend #gamma
      }
    }
  }
}

views {
  deployment prod {
    view rel_only_next {
      include relationship * where source.tag is #next
    }

    view rel_only_gamma {
      include relationship * where source.tag is #gamma
    }

    view rel_only_missing {
      include relationship * where source.tag is #missing
    }
  }
}
```

Expected rendering behavior:
- `rel_only_next`: shows the `reads` relation.
- `rel_only_gamma`: shows the `reads` relation.
- `rel_only_missing`: renders empty.# Deployment-Instance Cumulative Tags — Fixture

Below is a single paste-ready `.c4` file that proves deployment-instance tags are
cumulative for `source.tag` filtering.

**Key claim being proved:**  
`prod.eu.web.frontend` is an instance of the logical element `frontend` (tagged `#next`).
The instance itself adds `#gamma`. LikeC4 merges both sets of tags, so the instance
carries `{#next, #gamma}`. Views filtering on either tag therefore both render the `reads`
relation, while filtering on `#missing` renders nothing.

---

```likec4
// ── cumulative-tags-fixture.c4 ────────────────────────────────────────────

specification {
  element system
  deployment node zone
  tag #next
  tag #gamma
  tag #missing
}

// ── logical model ─────────────────────────────────────────────────────────

model {
  // #next comes from the logical element definition
  frontend = system 'Frontend' #next
  db       = system 'Database'

  frontend -> db 'reads'
}

// ── deployment ────────────────────────────────────────────────────────────

deployment {
  prod = zone 'Production' {
    eu = zone 'EU' {
      web = zone 'Web Tier' {
        // This instance inherits #next from the logical 'frontend'
        // and gains #gamma here → effective tags = { #next, #gamma }
        frontend = instanceOf frontend #gamma
      }
    }
  }

  // plain instance of db — no extra tags
  db_inst = instanceOf db
}

// ── views ─────────────────────────────────────────────────────────────────

views {

  // RENDERS: prod.eu.web.frontend has #next (inherited) → 'reads' relation visible
  deployment view rel_only_next {
    title "Filtered by #next — expects 'reads'"
    include * -> * where source.tag is #next
  }

  // RENDERS: prod.eu.web.frontend has #gamma (own) → 'reads' relation visible
  deployment view rel_only_gamma {
    title "Filtered by #gamma — expects 'reads'"
    include * -> * where source.tag is #gamma
  }

  // EMPTY: no instance carries #missing → no edges rendered
  deployment view rel_only_missing {
    title "Filtered by #missing — expects empty"
    include * -> * where source.tag is #missing
  }

}
```

---

## Why each view behaves as expected

| View | Filter | Instance tags on `prod.eu.web.frontend` | Match? | Result |
|---|---|---|---|---|
| `rel_only_next` | `source.tag is #next` | `{#next, #gamma}` — `#next` present | ✅ | `reads` rendered |
| `rel_only_gamma` | `source.tag is #gamma` | `{#next, #gamma}` — `#gamma` present | ✅ | `reads` rendered |
| `rel_only_missing` | `source.tag is #missing` | `{#next, #gamma}` — `#missing` absent | ❌ | empty |

The `db_inst` instance never appears as a *source* (it is always the target in the `reads`
relation), so it plays no role in source-tag filtering here.

## How tag inheritance works

In LikeC4, when a logical element is deployed, the resulting instance holds the union of:

1. Tags declared on the **logical element** (here `#next` on `frontend`).
2. Tags declared on the **deployed instance** (here `#gamma` on `prod.eu.web.frontend`).

This union is used when evaluating `where source.tag is …` predicates in deployment views,
which is exactly what this fixture exercises.
