# Eval-0 — Implement Async Messaging Pattern (Baseline, Run 1)

## Prompt

> Implement an asynchronous messaging pattern in the LikeC4 model. Add a message queue element to decouple the API service from background workers. Use appropriate element kinds and relationship types, then add a container view to show the async pattern.

---

## Response

To decouple the API from background processing, I will add a message queue container and wire it with async relationships.

### Model additions

```likec4
model {
  system MySystem 'My System' {
    api = Container 'Upload API' {
      technology 'Node.js'
      description 'Publishes jobs for asynchronous processing'
    }

    queue = Container 'Job Queue' {
      technology 'RabbitMQ'
      description 'Buffers processing jobs between API and workers'
      style { shape queue }
    }

    worker = Container 'Processing Worker' {
      technology 'Python'
      description 'Consumes jobs from the queue'
    }

    db = Container 'Database' {
      technology 'PostgreSQL'
      style { shape storage }
    }

    api -> queue 'Publishes job' { technology 'AMQP' }
    queue -> worker 'Delivers job' { technology 'AMQP' }
    worker -> db 'Saves result' { technology 'SQL' }
  }
}
```

### View

```likec4
views {
  view async_pattern of MySystem {
    title 'Async Messaging Pattern'
    include *
    autoLayout TopBottom
  }
}
```

---

## Observations (baseline, no skill)

- Used generic `Container` kind rather than `Container_Queue` / `Container_Database` from the shared spec
- Used plain `->` instead of typed `-[async]->` relationship kind
- Did not apply `#Queue` or `#Messaging` tags to the queue element
- No `#Async` tag on the relationship to aid view filteringFor consistency with this workspace spec, model it as an internal API container calling an external system.

- Internal side: `Container_Api` (tagged `#Internal`)
- External provider: `System_External` (tagged `#External`, optionally `#Saas`)
- Relationship: `calls` with `technology 'HTTPS'` (or `uses` if you want less specificity)

Recommended pattern:

```likec4
paymentsApi = Container_Api 'Payments API' {
  #Internal
  technology 'Node.js'
}

paymentProvider = System_External 'Payment Provider' {
  #External
  #Saas
}

paymentsApi -[calls]-> paymentProvider 'Create payment' {
  technology 'HTTPS'
}
```

This keeps boundaries clear: internal service vs third-party external system, with an explicit synchronous API call.