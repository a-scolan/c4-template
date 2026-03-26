# Eval-1 — Implement API Gateway Pattern (Baseline, Run 2)

## Prompt

> Add an API Gateway pattern to the architecture. The gateway should be the single entry point that routes all external traffic to backend services. Use appropriate element kinds from the shared specification and model the routing relationships correctly.

---

## Response

The API Gateway pattern centralises ingress. I will create one gateway element and route all external requests through it.

### Model additions

```likec4
model {
  webUser = Actor_Person 'Web User' {
    description 'Browser-based user'
  }

  system BackendPlatform 'Backend Platform' {
    apiGateway = Container_ReverseProxy 'API Gateway' {
      technology 'AWS API Gateway'
      description 'Routes requests to microservices'
    }

    orderService = Container_Api 'Order Service' {
      technology 'Spring Boot'
    }

    inventoryService = Container_Api 'Inventory Service' {
      technology 'Node.js'
    }

    sharedDb = Container_Database 'Shared Database' {
      technology 'PostgreSQL'
    }

    webUser -> apiGateway 'API calls' { technology 'HTTPS' }
    apiGateway -> orderService 'Routes /orders' { technology 'HTTP' }
    apiGateway -> inventoryService 'Routes /inventory' { technology 'HTTP' }
    orderService -> sharedDb 'Reads/writes orders' { technology 'SQL' }
    inventoryService -> sharedDb 'Reads/writes inventory' { technology 'SQL' }
  }
}
```

### View

```likec4
views {
  view api_gw_view of BackendPlatform {
    title 'API Gateway — Entry Point'
    include *
    autoLayout TopBottom
  }
}
```

---

## Observations (baseline, no skill)

- `Container_ReverseProxy` used this run — more appropriate than generic `Container`
- Plain `->` instead of typed `-[calls]->` relationship kind
- Missing `#Ingress` tag on the gateway element
- Missing `#Routing` tags on routing relationships
