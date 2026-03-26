# Eval-1 — Implement API Gateway Pattern (Baseline, Run 1)

## Prompt

> Add an API Gateway pattern to the architecture. The gateway should be the single entry point that routes all external traffic to backend services. Use appropriate element kinds from the shared specification and model the routing relationships correctly.

---

## Response

I will add an API gateway element in front of the backend services. All external clients will route through this single entry point, which then forwards requests to the appropriate backend service.

### Model additions

```likec4
model {
  customer = Actor_Person 'Customer' {
    description 'External user accessing the system'
  }

  system Platform 'Platform' {
    gateway = Container 'API Gateway' {
      technology 'Kong'
      description 'Single entry point routing requests to downstream services'
    }

    authService = Container_Api 'Auth Service' {
      technology 'OAuth2'
    }

    userService = Container_Api 'User Service' {
      technology 'Node.js'
    }

    dataService = Container_Api 'Data Service' {
      technology 'Python'
    }

    database = Container_Database 'Main Database' {
      technology 'PostgreSQL'
    }

    customer -> gateway 'Sends requests' { technology 'HTTPS' }
    gateway -> authService 'Routes auth' { technology 'HTTP' }
    gateway -> userService 'Routes user ops' { technology 'HTTP' }
    gateway -> dataService 'Routes data ops' { technology 'HTTP' }
    authService -> database 'Reads' { technology 'SQL' }
    userService -> database 'Reads/writes' { technology 'SQL' }
    dataService -> database 'Reads/writes' { technology 'SQL' }
  }
}
```

### View

```likec4
views {
  view gateway_view of Platform {
    title 'API Gateway Pattern'
    include *
    autoLayout TopBottom
  }
}
```

---

## Observations (baseline, no skill)

- Used generic `Container` for the gateway instead of `Container_ReverseProxy` from shared spec
- Plain `->` arrows instead of typed `-[calls]->` or `-[uses]->`
- Missing `#Routing`, `#Ingress` tags that would help with view filtering
- Actor modeled correctly with `Actor_Person`Apply the standard producer/queue/consumer pattern.

- Producer: `Container_Api`
- Broker: `Container_Queue` with `technology 'RabbitMQ'`
- Consumer: worker container (`Container_Webapp` or `Container_ProcessingServer`)

Recommended pattern:

# Eval-1 — Implement API Gateway Pattern (Baseline, Run 1)

## Prompt

> Add an API Gateway pattern to the architecture. The gateway should be the single entry point that routes all external traffic to backend services. Use appropriate element kinds from the shared specification and model the routing relationships correctly.

---

## Response

I will add an API gateway element in front of the backend services. All external clients will route through this single entry point, which then forwards requests to the appropriate backend service.

### Model additions

```likec4
model {
  customer = Actor_Person 'Customer' {
    description 'External user accessing the system'
  }

  system Platform 'Platform' {
    gateway = Container 'API Gateway' {
      technology 'Kong'
      description 'Single entry point routing requests to downstream services'
    }

    authService = Container_Api 'Auth Service' {
      technology 'OAuth2'
    }

    userService = Container_Api 'User Service' {
      technology 'Node.js'
    }

    dataService = Container_Api 'Data Service' {
      technology 'Python'
    }

    database = Container_Database 'Main Database' {
      technology 'PostgreSQL'
    }

    customer -> gateway 'Sends requests' { technology 'HTTPS' }
    gateway -> authService 'Routes auth' { technology 'HTTP' }
    gateway -> userService 'Routes user ops' { technology 'HTTP' }
    gateway -> dataService 'Routes data ops' { technology 'HTTP' }
    authService -> database 'Reads' { technology 'SQL' }
    userService -> database 'Reads/writes' { technology 'SQL' }
    dataService -> database 'Reads/writes' { technology 'SQL' }
  }
}
```

### View

```likec4
views {
  view gateway_view of Platform {
    title 'API Gateway Pattern'
    include *
    autoLayout TopBottom
  }
}
```

---

## Observations (baseline, no skill)

- Used generic `Container` for the gateway instead of `Container_ReverseProxy` from shared spec
- Plain `->` arrows instead of typed `-[calls]->` or `-[uses]->`
- Missing `#Routing`, `#Ingress` tags that would help with view filtering
- Actor modeled correctly with `Actor_Person`
 — Implement API Gateway Pattern (Baseline, Run 1)

## Prompt

> Add an API Gateway pattern to the architecture. The gateway should be the single entry point that routes all external traffic to backend services. Use appropriate element kinds from the shared specification and model the routing relationships correctly.

---

## Response

I will add an API gateway element in front of the backend services. All external clients will route through this single entry point, which then forwards requests to the appropriate backend service.

### Model additions

```likec4
model {
  customer = Actor_Person 'Customer' {
    description 'External user accessing the system'
  }

  system Platform 'Platform' {
    gateway = Container 'API Gateway' {
      technology 'Kong'
      description 'Single entry point routing requests to downstream services'
    }

    authService = Container_Api 'Auth Service' {
      technology 'OAuth2'
    }

    userService = Container_Api 'User Service' {
      technology 'Node.js'
    }

    dataService = Container_Api 'Data Service' {
      technology 'Python'
    }

    database = Container_Database 'Main Database' {
      technology 'PostgreSQL'
    }

    customer -> gateway 'Sends requests' { technology 'HTTPS' }
    gateway -> authService 'Routes auth' { technology 'HTTP' }
    gateway -> userService 'Routes user ops' { technology 'HTTP' }
    gateway -> dataService 'Routes data ops' { technology 'HTTP' }
    authService -> database 'Reads' { technology 'SQL' }
    userService -> database 'Reads/writes' { technology 'SQL' }
    dataService -> database 'Reads/writes' { technology 'SQL' }
  }
}
```

### View

```likec4
views {
  view gateway_view of Platform {
    title 'API Gateway Pattern'
    include *
    autoLayout TopBottom
  }
}
```

---

## Observations (baseline, no skill)

- Used generic `Container` for the gateway instead of `Container_ReverseProxy` from shared spec
- Plain `->` arrows instead of typed `-[calls]->` or `-[uses]->`
- Missing `#Routing`, `#Ingress` tags that would help with view filtering
- Actor modeled correctly with `Actor_Person`

api = Container_Api 'Jobs API' {
  #Internal
}

jobQueue = Container_Queue 'Job Queue' {
  #Queue
  technology 'RabbitMQ'
}

worker = Container_ProcessingServer 'Job Worker' {
  #Internal
}

api -[async]-> jobQueue 'Publishes job' {
  technology 'AMQP'
}

worker -[reads]-> jobQueue 'Consumes job' {
  technology 'AMQP'
}
```

Mistake to avoid: modeling this as a direct synchronous `calls` from API to worker (or bypassing the queue). That removes the async decoupling you are trying to represent.