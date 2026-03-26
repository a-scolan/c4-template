# Eval-1 — Implement API Gateway Pattern (Baseline, Run 3)

## Prompt

> Add an API Gateway pattern to the architecture. The gateway should be the single entry point that routes all external traffic to backend services. Use appropriate element kinds from the shared specification and model the routing relationships correctly.

---

## Response

I'll add a gateway container to act as the single public-facing entry point, forwarding all request traffic to backend services based on path routing.

### Model additions

```likec4
model {
  externalUser = Actor_Person 'External User'

  system ServicePlatform 'Service Platform' {
    gw = Container 'Gateway' {
      technology 'Nginx'
      description 'Reverse-proxy and router'
    }

    serviceA = Container_Api 'Service A' {
      technology 'Python'
    }

    serviceB = Container_Api 'Service B' {
      technology 'Go'
    }

    cache = Container 'Cache' {
      technology 'Redis'
    }

    db = Container_Database 'Database' {
      technology 'MySQL'
    }

    externalUser -> gw 'HTTP request' { technology 'HTTPS' }
    gw -> serviceA 'Routes /a' { technology 'HTTP' }
    gw -> serviceB 'Routes /b' { technology 'HTTP' }
    serviceA -> cache 'Reads cache' { technology 'Redis' }
    serviceA -> db 'Queries' { technology 'SQL' }
    serviceB -> db 'Queries' { technology 'SQL' }
  }
}
```

### View

```likec4
views {
  view svc_platform of ServicePlatform {
    title 'Gateway + Services'
    include *
    autoLayout TopBottom
  }
}
```

---

## Observations (baseline, no skill)

- Used generic `Container` for gateway (should be `Container_ReverseProxy`)
- No typed relationship kinds for routing
- Cache element added in this run as bonus but doesn't use `Container_Queue` or `#Queue` tags
