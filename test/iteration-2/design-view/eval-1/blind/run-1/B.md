Use a deployment-focused view with explicit tier boundaries and deployed instances.

LikeC4 approach aligned with workspace conventions:

- Environment: `Production`
- Zones:
  - `Dmz` (internet edge, gateway/reverse proxy)
  - `AppTier` (application services)
  - `DataTier` (database/storage)
- Nodes:
  - DMZ VM(s): gateway/web entry
  - App VM(s): API/app services (`instanceOf` logical containers)
  - Data VM(s): database/storage (`instanceOf` logical containers)
- Deployment relationships:
  - Internet/DMZ ingress (HTTPS)
  - DMZ -> AppTier (internal app protocol)
  - AppTier -> DataTier (DB/storage protocol)

Keep regular business traffic modeled in logical relationships and use deployment relationships for infrastructure-specific routing/security details.Use a **Deployment view** with explicit tiered deployment nodes: **DMZ**, **App Tier**, **Data Tier**.

Workspace-aligned approach:
- Keep logical elements in model files.
- Define deployment structure in deployment-focused files (as in `projects/shared/spec-deployment.c4` style).
- Add one production deployment view with clear grouping.

Example:

```likec4
model {
  user = person "User"

  systemA = system "Platform" {
    web = container "Web App"
    api = container "API"
    db = container "PostgreSQL"
  }

  extMail = system "External Email Service"

  user -> systemA.web "Uses"
  systemA.api -> extMail "Sends email"
}

deployment {
  environment prod {
    node internet "Internet" {
      instance user
    }

    node dmz "DMZ" {
      node lb "Load Balancer"
      instance systemA.web
    }

    node app_tier "App Tier" {
      node app_cluster "Kubernetes Cluster" {
        instance systemA.api
      }
    }

    node data_tier "Data Tier" {
      node db_host "DB Host" {
        instance systemA.db
      }
    }

    node external "External Services" {
      instance extMail
    }
  }
}

views {
  deployment view prod_infra {
    title "Production Infrastructure - DMZ / App / Data"
    include prod.*
  }
}
```

This gives a production-ready tiered structure while preserving C4 separation between logical model and runtime deployment.