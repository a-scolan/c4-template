Use **both**, with distinct responsibilities:

- **Deployment view** (mandatory for this request):
  - Model `SecZone` explicitly with bastion, firewall, and dedicated services
  - Keep infrastructure boundaries and network controls visible

- **C2 view** (recommended companion):
  - Show how security-facing application containers interact with core containers
  - Keep system-level responsibilities understandable to non-infra readers

Cleanest approach:
- Deployment view answers “where and how secured in production”
- C2 answers “what interacts with what at container level”

So the minimal complete documentation is: Deployment for `SecZone` + one focused C2 for container interactions.Use **both**: a focused **Deployment view** and a complementary **C2 Container view**.

Cleanest approach:
- **C2** answers: *what logical services exist in SecZone and how they interact*.
- **Deployment** answers: *where bastion/firewall/dedicated services are physically deployed in production*.

For your case (`SecZone`, bastion, firewall, dedicated services):
1. Add/confirm logical containers (e.g., `access-gateway`, `sec-service-a`, `sec-service-b`) in C2.
2. Model production deployment nodes under `SecZone`:
   - `bastion`
   - `firewall`
   - secure app hosts / cluster for dedicated services
3. Create two views:
   - `c2_seczone` (logical)
   - `deploy_prod_seczone` (physical/runtime)

Minimal skeleton:

```likec4
model {
  platform = system "Platform" {
    secGateway = container "Security Access Gateway"
    secSvcA = container "Dedicated Security Service A"
    secSvcB = container "Dedicated Security Service B"
  }

  secGateway -> secSvcA "Routes secured traffic"
  secGateway -> secSvcB "Routes secured traffic"
}

deployment {
  environment prod {
    node seczone "SecZone" {
      node bastion "Bastion"
      node firewall "Firewall"
      node secure_apps "Secure Services Cluster" {
        instance platform.secGateway
        instance platform.secSvcA
        instance platform.secSvcB
      }
    }
  }
}

views {
  view c2_seczone of platform {
    include platform.*
    title "C2 - SecZone Services"
  }

  deployment view deploy_prod_seczone {
    include prod.seczone.*
    title "Production Deployment - SecZone"
  }
}
```

Decision: **both views** is the most maintainable and audit-friendly option.