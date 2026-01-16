---
name: model-deployment
description: Model deployment infrastructure (environments, zones, VMs, apps) with proper hierarchy and instanceOf links.
---

# Model Deployment Infrastructure

Use this skill when defining physical infrastructure in deployment.c4.

## Structure

```
Node_Environment (Production/Development)
  └─ Zone (VLAN/Network segment)
      └─ Node_Vm/Node_Server
          └─ Node_App (instanceOf Container from model)
```

## Requirements

1. **PascalCase variables:** Use `ProdApiVm` not `prod_api_vm` in deployment
2. **InstanceOf:** Link `Node_App` to model Container using FQN
3. **Infrastructure relationships:** Use `https`, `tcp`, etc. with port descriptions
4. **Port format:** Use `"any -> 443"` or `"8080 -> 8080"` in description blocks
5. **Deployment tags:** Use #Production, #Networking, #Service, #Monitoring (from spec-deployment.c4)

## Example

```likec4
deployment {
  Prod = Node_Environment 'Production' {
    #Production
    
    AppTier = Zone 'App Tier (VLAN 200)' {
      #Networking
      
      ApiVm = Node_Vm 'prod-api-01' {
        technology 'Ubuntu 22.04, 8 vCPU, 16GB RAM'
        description 'API service host'
        
        ApiApp = Node_App 'API Application' {
          instanceOf mySystem.api
        }
      }
    }
  }
}

Prod.AppTier.ApiVm -[https]-> Prod.DataTier.DbVm 'Database queries' {
  description "any -> 5432"
}
```
